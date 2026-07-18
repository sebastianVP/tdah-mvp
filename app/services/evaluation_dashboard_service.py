from sqlalchemy import func
import pandas as pd

from app.database.db import SessionLocal
from app.database.models import Participant, Evaluation

from app.services.pdf_service import generate_pdf

from app.services.email_service import send_result_email

import os

# ==========================================================
# TOTAL DE EVALUACIONES
# ==========================================================

def get_total_evaluations():

    db = SessionLocal()

    try:

        total = db.query(

            func.count(Evaluation.id)

        ).scalar()

        return total or 0

    finally:

        db.close()
        
# ==========================================================
# TOTAL RIESGO ALTO
# ==========================================================

def get_total_high_risk():

    db = SessionLocal()

    try:

        total = db.query(

            func.count(Evaluation.id)

        ).filter(

            Evaluation.probability_level == "Alto"

        ).scalar()

        return total or 0

    finally:

        db.close()

# ==========================================================
# TOTAL RIESGO MODERADO
# ==========================================================

def get_total_medium_risk():

    db = SessionLocal()

    try:

        total = db.query(

            func.count(Evaluation.id)

        ).filter(

            Evaluation.probability_level == "Moderado"

        ).scalar()

        return total or 0

    finally:

        db.close()

# ==========================================================
# TOTAL RIESGO BAJO
# ==========================================================

def get_total_low_risk():

    db = SessionLocal()

    try:

        total = db.query(

            func.count(Evaluation.id)

        ).filter(

            Evaluation.probability_level == "Bajo"

        ).scalar()

        return total or 0

    finally:

        db.close()

# ==========================================================
# TODAS LAS EVALUACIONES
# ==========================================================

def get_all_evaluations():

    db = SessionLocal()

    try:

        rows = (

            db.query(

                Evaluation.id,

                Evaluation.created_at,

                Participant.full_name,

                Participant.email,

                Evaluation.score,

                Evaluation.max_score,

                Evaluation.probability_level

            )

            .join(

                Participant,

                Participant.id == Evaluation.participant_id

            )

            .order_by(

                Evaluation.created_at.desc()

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

                "Puntaje",

                "Máximo",

                "Riesgo"

            ]

        )

        return df

    finally:

        db.close()

# ==========================================================
# BUSCAR EVALUACIONES
# ==========================================================

def search_evaluations(search_text):

    db = SessionLocal()

    try:

        rows = (

            db.query(

                Evaluation.id,

                Evaluation.created_at,

                Participant.full_name,

                Participant.email,

                Evaluation.score,

                Evaluation.max_score,

                Evaluation.probability_level

            )

            .join(

                Participant,

                Participant.id == Evaluation.participant_id

            )

            .filter(

                (Participant.full_name.ilike(f"%{search_text}%")) |

                (Participant.email.ilike(f"%{search_text}%"))

            )

            .order_by(

                Evaluation.created_at.desc()

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

                "Puntaje",

                "Máximo",

                "Riesgo"

            ]

        )

        return df

    finally:

        db.close()

# ==========================================================
# EXPORTAR EXCEL
# ==========================================================

def export_excel():

    df = get_all_evaluations()

    return df.to_excel(

        "Evaluaciones.xlsx",

        index=False

    )

# ==========================================================
# EXPORTAR CSV
# ==========================================================

def export_csv():

    df = get_all_evaluations()

    return df.to_csv(

        "Evaluaciones.csv",

        index=False,

        encoding="utf-8-sig"

    )

# ==========================================================
# OBTENER EVALUACIÓN POR ID
# ==========================================================

def get_evaluation_by_id(evaluation_id):

    db = SessionLocal()

    try:

        evaluation = (

            db.query(

                Evaluation,

                Participant

            )

            .join(

                Participant,

                Participant.id == Evaluation.participant_id

            )

            .filter(

                Evaluation.id == evaluation_id

            )

            .first()

        )

        return evaluation

    finally:

        db.close()

# ==========================================================
# ELIMINAR EVALUACIÓN
# ==========================================================

def delete_evaluation(evaluation_id):

    db = SessionLocal()

    try:

        evaluation = (

            db.query(

                Evaluation

            )

            .filter(

                Evaluation.id == evaluation_id

            )

            .first()

        )

        if evaluation is None:

            return False

        db.delete(evaluation)

        db.commit()

        return True

    finally:

        db.close()

# ==========================================================
# RESPUESTAS DEL CUESTIONARIO
# ==========================================================

def get_responses(evaluation_id):

    db = SessionLocal()

    try:

        responses = (

            db.query(

                Evaluation.responses

            )

            .filter(

                Evaluation.id == evaluation_id

            )

            .scalar()

        )

        return responses

    finally:

        db.close()

# ==========================================================
# DATOS PARA PDF
# ==========================================================

def get_pdf_data(evaluation_id):

    db = SessionLocal()

    try:

        row = (

            db.query(

                Participant.full_name,

                Participant.email,

                Participant.age,

                Participant.gender,

                Evaluation.score,

                Evaluation.max_score,

                Evaluation.probability_level,

                Evaluation.responses

            )

            .join(

                Participant,

                Participant.id == Evaluation.participant_id

            )

            .filter(

                Evaluation.id == evaluation_id

            )

            .first()

        )

        return row

    finally:

        db.close()

# ==========================================================
# DATOS PARA REENVIAR CORREO
# ==========================================================

def get_email_data(evaluation_id):

    db = SessionLocal()

    try:

        row = (

            db.query(

                Participant.email,

                Participant.full_name,

                Evaluation.score,

                Evaluation.probability_level

            )

            .join(

                Participant,

                Participant.id == Evaluation.participant_id

            )

            .filter(

                Evaluation.id == evaluation_id

            )

            .first()

        )

        return row

    finally:

        db.close()

# ==========================================================
# REGENERAR PDF
# ==========================================================

def regenerate_pdf(evaluation_id):

    data = get_pdf_data(evaluation_id)

    if data is None:

        return None

    (
        full_name,
        email,
        age,
        gender,
        score,
        max_score,
        risk,
        responses
    ) = data



    filename = f"evaluation_{evaluation_id}.pdf"

    generate_pdf(
        filename=filename,

        participant=full_name,

        email=email,

        age=age,

        gender=gender,

        score=score,

        risk=risk,

        evaluation_id=evaluation_id

    )

    return os.path.join(

        "reports",

        filename

    )

# ==========================================================
# REENVIAR CORREO
# ==========================================================

def resend_email(evaluation_id):

    data = get_pdf_data(evaluation_id)

    if data is None:

        return

    (
        full_name,
        email,
        age,
        gender,
        score,
        max_score,
        risk,
        responses

    ) = data

    pdf_path = regenerate_pdf(evaluation_id)

    send_result_email(

        recipient=email,

        score=score,

        risk=risk,

        pdf_path=pdf_path,

        evaluation_id=evaluation_id

    )

    return True

# ==========================================================
# ELIMINAR EVALUACIÓN
# ==========================================================

def delete_evaluation(evaluation_id):

    db = SessionLocal()

    try:

        evaluation = (

            db.query(Evaluation)

            .filter(

                Evaluation.id == evaluation_id

            )

            .first()

        )

        if evaluation is None:

            return False

        db.delete(evaluation)

        db.commit()

        return True

    except Exception:

        db.rollback()

        return False

    finally:

        db.close()


# ==========================================================
# DETALLE DE EVALUACIÓN
# ==========================================================

def get_evaluation_detail(evaluation_id):

    db = SessionLocal()

    try:

        row = (

            db.query(

                Evaluation,

                Participant

            )

            .join(

                Participant,

                Participant.id == Evaluation.participant_id

            )

            .filter(

                Evaluation.id == evaluation_id

            )

            .first()

        )

        return row

    finally:

        db.close()