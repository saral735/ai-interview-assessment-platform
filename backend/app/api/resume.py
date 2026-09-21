
import io
import os
import uuid
import zipfile

import fitz
from docx import Document

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_role
from app.models.candidate import Candidate


router = APIRouter(
    prefix="/resumes",
    tags=["Resumes"]
)


UPLOAD_DIR = "uploads/resumes"

os.makedirs(UPLOAD_DIR, exist_ok=True)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx"
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_file_content(
    file_content: bytes,
    file_extension: str
) -> bool:

    if file_extension == ".pdf":
        return file_content.startswith(b"%PDF-")

    if file_extension == ".docx":

        try:
            with zipfile.ZipFile(
                io.BytesIO(file_content)
            ) as archive:

                file_names = archive.namelist()

                return (
                    "[Content_Types].xml" in file_names
                    and "word/document.xml" in file_names
                )

        except zipfile.BadZipFile:
            return False

    return False


def extract_pdf_text(file_content: bytes) -> str:

    text_parts = []

    with fitz.open(
        stream=file_content,
        filetype="pdf"
    ) as document:

        for page in document:
            text_parts.append(page.get_text())

    return "\n".join(text_parts).strip()


def extract_docx_text(file_content: bytes) -> str:

    document = Document(
        io.BytesIO(file_content)
    )

    text_parts = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(text_parts).strip()


def extract_resume_text(
    file_content: bytes,
    file_extension: str
) -> str:

    if file_extension == ".pdf":
        return extract_pdf_text(file_content)

    if file_extension == ".docx":
        return extract_docx_text(file_content)

    return ""


@router.post("/upload")
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("candidate")
    )
):

    user_id = int(current_user["sub"])

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required"
        )

    file_extension = os.path.splitext(
        file.filename
    )[1].lower()

    if file_extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed"
        )

    file_content = file.file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty"
        )

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must not exceed 5 MB"
        )

    if not validate_file_content(
        file_content,
        file_extension
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid or corrupted PDF/DOCX file"
        )

    try:

        resume_text = extract_resume_text(
            file_content,
            file_extension
        )

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Unable to extract text from resume"
        )

    if not resume_text:
        raise HTTPException(
            status_code=400,
            detail="No readable text found in resume"
        )

    unique_filename = (
        f"{uuid.uuid4()}{file_extension}"
    )

    file_path = os.path.join(
        UPLOAD_DIR,
        unique_filename
    )

    old_file_path = None

    candidate = db.query(Candidate).filter(
        Candidate.user_id == user_id
    ).first()

    if candidate:
        old_file_path = candidate.resume_file

    try:

        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        if not candidate:

            candidate = Candidate(
                name="Candidate",
                email=current_user.get(
                    "email",
                    ""
                ),
                user_id=user_id,
                resume_file=file_path,
                resume_text=resume_text
            )

            db.add(candidate)

        else:

            candidate.resume_file = file_path
            candidate.resume_text = resume_text

        db.commit()
        db.refresh(candidate)

    except Exception:

        db.rollback()

        if os.path.exists(file_path):
            os.remove(file_path)

        raise HTTPException(
            status_code=500,
            detail="Failed to save resume"
        )

    if old_file_path and old_file_path != file_path:

        if os.path.exists(old_file_path):
            os.remove(old_file_path)

    return {
        "message": "Resume uploaded and parsed successfully",
        "candidate_id": candidate.id,
        "file_name": unique_filename,
        "text_length": len(resume_text)
    }
