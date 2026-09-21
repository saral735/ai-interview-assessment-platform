
import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse
from app.core.security import create_access_token


router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
def login(user: LoginRequest, db: Session = Depends(get_db)):

    existing_user = db.query(User).filter(User.email == user.email).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_valid = bcrypt.checkpw(
        user.password.encode("utf-8"),
        existing_user.password_hash.encode("utf-8")
    )

    if not password_valid:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
    {
        "sub": str(existing_user.id),
        "role": existing_user.role,
        "email": existing_user.email
    }
)

    return {
        "message": "Login successful",
        "user_id": existing_user.id,
        "role": existing_user.role,
        "access_token": access_token
    }
