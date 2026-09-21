from sqlalchemy import Column, Integer, Float, Text, ForeignKey

from app.core.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    answer_id = Column(
        Integer,
        ForeignKey("answers.id"),
        nullable=False
    )

    technical_score = Column(
        Float,
        default=0.0
    )

    problem_solving_score = Column(
        Float,
        default=0.0
    )

    project_score = Column(
        Float,
        default=0.0
    )

    communication_score = Column(
        Float,
        default=0.0
    )

    behavioral_score = Column(
        Float,
        default=0.0
    )

    overall_score = Column(
        Float,
        default=0.0
    )

    feedback = Column(
        Text,
        nullable=True
    )