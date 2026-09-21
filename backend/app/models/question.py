
from sqlalchemy import Column, Integer, String, Text, ForeignKey

from app.core.database import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    interview_id = Column(
        Integer,
        ForeignKey("interviews.id"),
        nullable=False,
        index=True
    )

    question_text = Column(
        Text,
        nullable=False
    )

    question_type = Column(
        String(50),
        nullable=False
    )

    difficulty = Column(
        String(50),
        nullable=False,
        default="medium"
    )

    question_order = Column(
        Integer,
        nullable=False
    )

    is_answered = Column(
        Integer,
        nullable=False,
        default=0
    )

