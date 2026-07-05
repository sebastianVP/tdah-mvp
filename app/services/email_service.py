import os
import smtplib

from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_result_email(
    recipient,
    score,
    risk
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

    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = recipient

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465
    ) as server:

        server.login(
            EMAIL_USER,
            EMAIL_PASSWORD
        )

        server.send_message(msg)