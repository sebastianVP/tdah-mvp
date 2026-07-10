from sqlalchemy import func

from app.database.db import SessionLocal
from app.database.models import Participant, Evaluation


# ==========================================
# TOTAL DE EVALUACIONES
# ==========================================

def get_total_evaluations():

    db = SessionLocal()

    try:

        total = db.query(
            func.count(Evaluation.id)
        ).scalar()

        return total or 0

    finally:

        db.close()


# ==========================================
# TOTAL PARTICIPANTES
# ==========================================

def get_total_participants():

    db = SessionLocal()

    try:

        total = db.query(
            func.count(Participant.id)
        ).scalar()

        return total or 0

    finally:

        db.close()


# ==========================================
# EDAD PROMEDIO
# ==========================================

def get_average_age():

    db = SessionLocal()

    try:

        average = db.query(
            func.avg(
                Participant.age
            )
        ).scalar()

        if average is None:

            return 0

        return round(float(average), 1)

    finally:

        db.close()


# ==========================================
# PORCENTAJE RIESGO ALTO
# ==========================================

def get_high_risk_percentage():

    db = SessionLocal()

    try:

        total = db.query(
            func.count(Evaluation.id)
        ).scalar()

        if total == 0:

            return 0

        high = db.query(
            func.count(Evaluation.id)
        ).filter(
            Evaluation.probability_level == "Alto"
        ).scalar()

        return round(
            high * 100 / total,
            1
        )

    finally:

        db.close()