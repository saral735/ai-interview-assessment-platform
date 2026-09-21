
from pydantic import BaseModel, Field


class EvaluationCreate(BaseModel):
    answer_id: int

    technical_score: float = Field(
        ge=0,
        le=100
    )

    problem_solving_score: float = Field(
        ge=0,
        le=100
    )

    project_score: float = Field(
        ge=0,
        le=100
    )

    communication_score: float = Field(
        ge=0,
        le=100
    )

    behavioral_score: float = Field(
        ge=0,
        le=100
    )

    overall_score: float = Field(
        ge=0,
        le=100
    )

    feedback: str | None = None


class EvaluationResponse(BaseModel):
    id: int
    answer_id: int

    technical_score: float
    problem_solving_score: float
    project_score: float
    communication_score: float
    behavioral_score: float

    overall_score: float

    feedback: str | None = None

    model_config = {
        "from_attributes": True
    }
