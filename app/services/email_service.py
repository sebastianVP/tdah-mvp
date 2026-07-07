import os
import smtplib

#from email.mime.text import MIMEText

from email.message import EmailMessage
from pathlib import Path
import mimetypes


from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


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

Resultado obtenido:

Puntaje: {score}

Nivel de riesgo: {risk}

Este resultado es únicamente orientativo y no constituye un diagnóstico médico.

Equipo MindAlert
"""

    #msg = MIMEText(body)

    #msg["Subject"] = subject
    #msg["From"] = EMAIL_USER
    #msg["To"] = recipient
    msg = EmailMessage()

    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = recipient

    msg.set_content(body)

    # ======================================================
    # Adjuntar Reporte PDF
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

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        server.login(
            EMAIL_USER,
            EMAIL_PASSWORD
        )

        server.send_message(msg)