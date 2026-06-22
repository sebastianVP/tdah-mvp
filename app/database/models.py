from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    Boolean,
)

from sqlalchemy import ForeignKey
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

    participant_id = Column(
        Integer,
        ForeignKey("participants.id")
    )

    score = Column(Integer)

    max_score = Column(Integer)

    probability_level = Column(String)

    responses = Column(JSON)

class Participant(Base):
    __tablename__ ="participants"

    id = Column(
        Integer,
        primary_key=True
    )

    created_at = Column(
        DateTime,
        default = datetime.utcnow
    )

    full_name = Column(
        String,
        nullable = False
    )

    age = Column(Integer)
    
    email = Column(String, unique=True, index=True)  # <--- ESTA ES LA COLUMNA QUE FALTA

    gender = Column(String)

    consent = Column(
        Boolean,
        default = False
    )