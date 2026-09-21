from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_role
from app.models.candidate import Candidate
from app.models.job import Job
from app.services.skill_matching import calculate_skill_match


router = APIRouter(
    prefix="/matching",
    tags=["Matching"]
)


@router.get("/candidate/{candidate_id}/job/{job_id}")
def match_candidate_with_job(
    candidate_id: int,
    job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(
        require_role("recruiter")
    )
):

    candidate = (
        db.query(Candidate)
        .filter(Candidate.id == candidate_id)
        .first()
    )

    if not candidate:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found"
        )

    job = (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.created_by == int(current_user["sub"])
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if not candidate.resume_text:
        raise HTTPException(
            status_code=400,
            detail="Candidate resume has not been parsed"
        )

    result = calculate_skill_match(
        required_skills=job.required_skills,
        preferred_skills=job.preferred_skills,
        resume_text=candidate.resume_text
    )

    return {
        "candidate_id": candidate.id,
        "job_id": job.id,
        "job_title": job.title,
        "matching": result
    }