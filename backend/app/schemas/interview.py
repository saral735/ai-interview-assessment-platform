from pydantic import BaseModel, ConfigDict


class InterviewCreate(BaseModel):
    candidate_id: int
    job_id: int


class InterviewResponse(BaseModel):
    id: int
    candidate_id: int
    job_id: int
    status: str

    model_config = ConfigDict(from_attributes=True)