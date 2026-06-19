from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Evaluation(Base):

    __tablename__ = "evaluations"

    id = Column(
        Integer,
        primary_key=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    score = Column(Integer)

    max_score = Column(Integer)

    probability_level = Column(String)

    responses = Column(JSON)