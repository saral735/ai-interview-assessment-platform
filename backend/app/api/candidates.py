from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models.candidate import Candidate


router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"]
)


@router.get("/")
def get_candidates(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_role("recruiter"))
):
    candidates = db.query(Candidate).all()

    return candidates