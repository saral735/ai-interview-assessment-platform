
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.permissions import require_role
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate, JobResponse


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)


@router.post(
    "/",
    response_model=JobResponse,
    status_code=201
)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("recruiter"))
):

    recruiter_id = int(current_user["sub"])

    new_job = Job(
        title=job.title,
        description=job.description,
        required_skills=job.required_skills,
        preferred_skills=job.preferred_skills,
        experience_years=job.experience_years,
        passing_score=job.passing_score,
        created_by=recruiter_id
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job


@router.get(
    "/",
    response_model=list[JobResponse]
)
def get_jobs(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("recruiter"))
):

    recruiter_id = int(current_user["sub"])

    jobs = (
        db.query(Job)
        .filter(Job.created_by == recruiter_id)
        .all()
    )

    return jobs


@router.get(
    "/{job_id}",
    response_model=JobResponse
)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("recruiter"))
):

    recruiter_id = int(current_user["sub"])

    job = (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.created_by == recruiter_id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job


@router.put(
    "/{job_id}",
    response_model=JobResponse
)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("recruiter"))
):

    recruiter_id = int(current_user["sub"])

    job = (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.created_by == recruiter_id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    update_data = job_data.model_dump(
        exclude_unset=True
    )

    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)

    return job


@router.delete(
    "/{job_id}"
)
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("recruiter"))
):

    recruiter_id = int(current_user["sub"])

    job = (
        db.query(Job)
        .filter(
            Job.id == job_id,
            Job.created_by == recruiter_id
        )
        .first()
    )

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully",
        "job_id": job_id
    }
