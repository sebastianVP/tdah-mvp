from pathlib import Path

from unittest.mock import patch


from app.services.email_service import send_result_email

from app.services.pdf_service import generate_pdf



def test_send_email_runs_without_exception():

    pdf_path = generate_pdf(

        filename="email_test.pdf",

        participant="Usuario Test",

        email="usuario@test.com",

        age=25,

        gender="Masculino",

        score=18,

        risk="Alto",

        evaluation_id=1

    )

    send_result_email(

        recipient="alex.valdezp22@gmail.com",

        score=18,

        risk="Alto",

        pdf_path=pdf_path,

        evaluation_id=1

    )

    assert True

@patch("smtplib.SMTP_SSL")

def test_send_email(mock_smtp):

    pdf_path = generate_pdf(

        filename="email_test.pdf",

        participant="Usuario Test",

        email="usuario@test.com",

        age=25,

        gender="Masculino",

        score=20,

        risk="Alto",

        evaluation_id=1

    )

    send_result_email(

        recipient="usuario@test.com",

        score=20,

        risk="Alto",

        pdf_path=pdf_path,

        evaluation_id=1

    )

    assert mock_smtp.called