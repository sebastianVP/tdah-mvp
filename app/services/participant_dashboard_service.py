from sqlalchemy import func
import pandas as pd

from app.database.db import SessionLocal
from app.database.models import Participant


# ==========================================================
# TODOS LOS PARTICIPANTES
# ==========================================================

def get_all_participants():

    db = SessionLocal()

    try:

        rows = (

            db.query(

                Participant.id,

                Participant.created_at,

                Participant.full_name,

                Participant.email,

                Participant.age,

                Participant.gender

            )

            .order_by(

                Participant.created_at.desc()

            )

            .all()

        )

        df = pd.DataFrame(

            rows,

            columns=[

                "ID",

                "Fecha",

                "Nombre",

                "Correo",

                "Edad",

                "Sexo"

            ]

        )

        return df

    finally:

        db.close()


# ==========================================================
# BUSCAR PARTICIPANTE
# ==========================================================

def search_participants(text):

    db = SessionLocal()

    try:

        rows = (

            db.query(

                Participant.id,

                Participant.created_at,

                Participant.full_name,

                Participant.email,

                Participant.age,

                Participant.gender

            )

            .filter(

                (Participant.full_name.ilike(f"%{text}%")) |

                (Participant.email.ilike(f"%{text}%"))

            )

            .order_by(

                Participant.created_at.desc()

            )

            .all()

        )

        df = pd.DataFrame(

            rows,

            columns=[

                "ID",

                "Fecha",

                "Nombre",

                "Correo",

                "Edad",

                "Sexo"

            ]

        )

        return df

    finally:

        db.close()


# ==========================================================
# TOTAL PARTICIPANTES
# ==========================================================

def get_total_participants():

    db = SessionLocal()

    try:

        total = db.query(

            func.count(Participant.id)

        ).scalar()

        return total or 0

    finally:

        db.close()


# ==========================================================
# TOTAL HOMBRES
# ==========================================================

def get_total_males():

    db = SessionLocal()

    try:

        total = (

            db.query(

                func.count(Participant.id)

            )

            .filter(

                Participant.gender == "Masculino"

            )

            .scalar()

        )

        return total or 0

    finally:

        db.close()


# ==========================================================
# TOTAL MUJERES
# ==========================================================

def get_total_females():

    db = SessionLocal()

    try:

        total = (

            db.query(

                func.count(Participant.id)

            )

            .filter(

                Participant.gender == "Femenino"

            )

            .scalar()

        )

        return total or 0

    finally:

        db.close()


# ==========================================================
# EDAD PROMEDIO
# ==========================================================

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

        return round(

            float(average),

            1

        )

    finally:

        db.close()


# ==========================================================
# PARTICIPANTE POR ID
# ==========================================================

def get_participant_by_id(participant_id):

    db = SessionLocal()

    try:

        participant = (

            db.query(

                Participant

            )

            .filter(

                Participant.id == participant_id

            )

            .first()

        )

        return participant

    finally:

        db.close()


# ==========================================================
# ELIMINAR PARTICIPANTE
# ==========================================================

def delete_participant(participant_id):

    db = SessionLocal()

    try:

        participant = (

            db.query(

                Participant

            )

            .filter(

                Participant.id == participant_id

            )

            .first()

        )

        if participant is None:

            return False

        db.delete(participant)

        db.commit()

        return True

    finally:

        db.close()


# ==========================================================
# EXPORTAR CSV
# ==========================================================

def export_csv():

    return get_all_participants()


# ==========================================================
# EXPORTAR EXCEL
# ==========================================================

def export_excel():

    return get_all_participants()