from pydantic import BaseModel, EmailStr


class CandidateBase(BaseModel):
    name: str
    email: EmailStr


class CandidateCreate(CandidateBase):
    pass


class CandidateResponse(CandidateBase):
    id: int
    resume_text: str | None = None
    resume_file: str | None = None
    user_id: int | None = None

    model_config = {
        "from_attributes": True
    }