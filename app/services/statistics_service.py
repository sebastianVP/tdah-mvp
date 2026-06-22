from sqlalchemy import func

from app.database.db import SessionLocal
from app.database.models import (
    Participant,
    Evaluation
)


def get_total_participants():

    db = SessionLocal()

    try:

        return db.query(
            Participant
        ).count()

    finally:

        db.close()


def get_total_evaluations():

    db = SessionLocal()

    try:

        return db.query(
            Evaluation
        ).count()

    finally:

        db.close()


def get_risk_distribution():

    db = SessionLocal()

    try:

        result = (
            db.query(
                Evaluation.probability_level,
                func.count(Evaluation.id)
            )
            .group_by(
                Evaluation.probability_level
            )
            .all()
        )

        return result

    finally:

        db.close()


def get_gender_distribution():

    db = SessionLocal()

    try:

        result = (
            db.query(
                Participant.gender,
                func.count(Participant.id)
            )
            .group_by(
                Participant.gender
            )
            .all()
        )

        return result

    finally:

        db.close()


def get_age_distribution():

    db = SessionLocal()

    try:

        participants = db.query(
            Participant
        ).all()

        groups = {
            "5-12": 0,
            "13-18": 0,
            "19-30": 0,
            "31-50": 0,
            "50+": 0
        }

        for p in participants:

            if p.age <= 12:
                groups["5-12"] += 1

            elif p.age <= 18:
                groups["13-18"] += 1

            elif p.age <= 30:
                groups["19-30"] += 1

            elif p.age <= 50:
                groups["31-50"] += 1

            else:
                groups["50+"] += 1

        return groups

    finally:

        db.close()