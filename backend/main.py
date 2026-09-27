from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.interviews import router as interviews_router
from app.core.database import Base, engine

from app.models import (
    User,
    Job,
    Candidate,
    Interview,
    Question,
    Answer,
    Evaluation
)

from app.api.jobs import router as jobs_router
from app.api.users import router as users_router
from app.api.auth import router as auth_router
from app.api.resume import router as resume_router
from app.api.matching import router as matching_router
from app.api.candidates import router as candidates_router

Base.metadata.create_all(bind=engine)


app = FastAPI()


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(users_router)

app.include_router(auth_router)

app.include_router(jobs_router)

app.include_router(resume_router)

app.include_router(matching_router)

app.include_router(interviews_router)

app.include_router(candidates_router)

@app.get("/")
def home():
    return {"message": "AI Interview Assessment API is running"}