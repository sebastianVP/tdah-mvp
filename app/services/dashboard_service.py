from sqlalchemy import func
import pandas as pd

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

# ==========================================================
# GRÁFICOS
# ==========================================================

def get_risk_distribution():

    db = SessionLocal()

    try:

        data = (

            db.query(

                Evaluation.probability_level,

                func.count(Evaluation.id)

            )

            .group_by(
                Evaluation.probability_level
            )

            .all()

        )

        return data

    finally:

        db.close()


# ==========================================================

def get_gender_distribution():

    db = SessionLocal()

    try:

        data = (

            db.query(

                Participant.gender,

                func.count(Participant.id)

            )

            .group_by(
                Participant.gender
            )

            .all()

        )

        return data

    finally:

        db.close()


# ==========================================================

def get_age_distribution():

    db = SessionLocal()

    try:

        participants = db.query(
            Participant.age
        ).all()

        ranges = {

            "18-25":0,

            "26-35":0,

            "36-45":0,

            "46+":0

        }

        for age_tuple in participants:

            age = age_tuple[0]

            if age is None:

                continue

            if 18 <= age <= 25:

                ranges["18-25"] += 1

            elif 26 <= age <= 35:

                ranges["26-35"] += 1

            elif 36 <= age <= 45:

                ranges["36-45"] += 1

            else:

                ranges["46+"] += 1

        return ranges

    finally:

        db.close()


# ==========================================================

def get_daily_evaluations():

    db = SessionLocal()

    try:

        data = (

            db.query(

                func.date(Evaluation.created_at),

                func.count(Evaluation.id)

            )

            .group_by(
                func.date(Evaluation.created_at)
            )

            .order_by(
                func.date(Evaluation.created_at)
            )

            .all()

        )

        return data

    finally:

        db.close()


# ==========================================================
# TABLA PRINCIPAL
# ==========================================================

def get_all_evaluations():

    db = SessionLocal()

    try:

        rows = (

            db.query(

                Evaluation.created_at,

                Participant.full_name,

                Participant.email,

                Participant.age,

                Participant.gender,

                Evaluation.score,

                Evaluation.max_score,

                Evaluation.probability_level

            )

            .join(

                Participant,

                Participant.id==Evaluation.participant_id

            )

            .order_by(

                Evaluation.created_at.desc()

            )

            .all()

        )

        df = pd.DataFrame(

            rows,

            columns=[

                "Fecha",

                "Nombre",

                "Correo",

                "Edad",

                "Sexo",

                "Puntaje",

                "Máximo",

                "Riesgo"

            ]

        )

        return df

    finally:

        db.close()


# ==========================================================
# BUSCADOR
# ==========================================================

def search_participant(text):

    db = SessionLocal()

    try:

        rows = (

            db.query(

                Evaluation.created_at,

                Participant.full_name,

                Participant.email,

                Participant.age,

                Participant.gender,

                Evaluation.score,

                Evaluation.max_score,

                Evaluation.probability_level

            )

            .join(

                Participant,

                Participant.id==Evaluation.participant_id

            )

            .filter(

                Participant.full_name.ilike(

                    f"%{text}%"

                )

            )

            .order_by(

                Evaluation.created_at.desc()

            )

            .all()

        )

        df = pd.DataFrame(

            rows,

            columns=[

                "Fecha",

                "Nombre",

                "Correo",

                "Edad",

                "Sexo",

                "Puntaje",

                "Máximo",

                "Riesgo"

            ]

        )

        return df

    finally:

        db.close()


# ==========================================================
# ACTIVIDAD RECIENTE
# ==========================================================

def get_recent_activity(limit=10):

    db = SessionLocal()

    try:

        rows = (

            db.query(

                Evaluation.created_at,

                Participant.full_name,

                Evaluation.probability_level,

                Evaluation.score

            )

            .join(

                Participant,

                Participant.id==Evaluation.participant_id

            )

            .order_by(

                Evaluation.created_at.desc()

            )

            .limit(limit)

            .all()

        )

        return rows

    finally:

        db.close()

def get_dashboard_table():

    db = SessionLocal()

    try:

        query = (

            db.query(

                Evaluation.created_at,

                Participant.full_name,

                Participant.email,

                Participant.gender,

                Participant.age,

                Evaluation.score,

                Evaluation.probability_level,

            )

            .join(

                Participant,

                Participant.id == Evaluation.participant_id

            )

            .order_by(

                Evaluation.created_at.desc()

            )

        )

        rows = query.all()

        df = pd.DataFrame(

            rows,

            columns=[

                "Fecha",

                "Nombre",

                "Correo",

                "Sexo",

                "Edad",

                "Puntaje",

                "Riesgo"

            ]

        )

        return df

    finally:

        db.close()