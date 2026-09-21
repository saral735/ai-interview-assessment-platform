
from pydantic import BaseModel, Field


class JobBase(BaseModel):
    title: str
    description: str
    required_skills: str | None = None
    preferred_skills: str | None = None
    experience_years: float | None = Field(
        default=None,
        ge=0
    )
    passing_score: float = Field(
        default=70.0,
        ge=0,
        le=100
    )


class JobCreate(JobBase):
    pass


class JobUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    required_skills: str | None = None
    preferred_skills: str | None = None
    experience_years: float | None = Field(
        default=None,
        ge=0
    )
    passing_score: float | None = Field(
        default=None,
        ge=0,
        le=100
    )


class JobResponse(JobBase):
    id: int
    created_by: int

    model_config = {
        "from_attributes": True
    }
