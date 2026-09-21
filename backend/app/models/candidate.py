
from sqlalchemy import Column, Integer, String, Text, ForeignKey

from app.core.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String(150),
        nullable=False
    )

    email = Column(
        String(150),
        nullable=False,
        index=True
    )

    resume_file = Column(
        String(255),
        nullable=True
    )

    resume_text = Column(
        Text,
        nullable=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        index=True
    )

