import os
import smtplib
import mimetypes

from pathlib import Path
from email.message import EmailMessage

from dotenv import load_dotenv

from app.services.settings_service import get_setting

load_dotenv()

# ======================================================
# CONFIGURACIÓN (FALLBACK)
# ======================================================

EMAIL_USER_ENV = os.getenv("EMAIL_USER")

EMAIL_PASSWORD_ENV = os.getenv("EMAIL_PASSWORD")

# ======================================================
# CONFIGURACIÓN DESDE SETTINGS
# ======================================================

SMTP_SERVER = get_setting("smtp_server") or "smtp.gmail.com"

SMTP_PORT = int(

    get_setting("smtp_port") or 465

)

EMAIL_USER = get_setting("smtp_email") or EMAIL_USER_ENV

EMAIL_PASSWORD = get_setting("smtp_password") or EMAIL_PASSWORD_ENV

# ======================================================
# ENVÍO DE CORREO
# ======================================================

def send_result_email(

    recipient,

    score,

    risk,

    pdf_path,

    evaluation_id

):

    subject = "Resultado de tu evaluación MindAlert"

    body = f"""
Hola,

Gracias por utilizar MindAlert.

Resultado obtenido

Puntaje: {score}

Nivel de riesgo: {risk}

Este resultado es únicamente orientativo y no constituye un diagnóstico médico.

Equipo MindAlert
"""

    msg = EmailMessage()

    msg["Subject"] = subject

    msg["From"] = EMAIL_USER

    msg["To"] = recipient

    msg.set_content(body)

    # ======================================================
    # Adjuntar PDF
    # ======================================================

    pdf_file = Path(pdf_path)

    mime_type, _ = mimetypes.guess_type(pdf_file)

    if mime_type is None:

        mime_type = "application/pdf"

    maintype, subtype = mime_type.split("/", 1)

    with open(pdf_file, "rb") as file:

        msg.add_attachment(

            file.read(),

            maintype=maintype,

            subtype=subtype,

            filename=f"MindAlert_Reporte_{evaluation_id}.pdf"

        )

    # ======================================================
    # Enviar
    # ======================================================

    with smtplib.SMTP_SSL(

        SMTP_SERVER,

        SMTP_PORT

    ) as server:

        server.login(

            EMAIL_USER,

            EMAIL_PASSWORD

        )

        server.send_message(msg)