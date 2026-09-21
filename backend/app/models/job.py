
from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey

from app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(150), nullable=False)

    description = Column(Text, nullable=False)

    required_skills = Column(Text, nullable=True)

    preferred_skills = Column(Text, nullable=True)

    experience_years = Column(Float, nullable=True)

    passing_score = Column(Float, default=70.0)

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
