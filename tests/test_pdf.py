from pathlib import Path

from app.services.pdf_service import generate_pdf

def test_generate_pdf_creates_file():

    pdf_path = generate_pdf(

        filename="report_test.pdf",

        participant="Usuario Test",

        email="usuario@test.com",

        age=25,

        gender="Masculino",

        score=15,

        risk="Moderado",

        evaluation_id=999

    )

    assert Path(pdf_path).exists()

def test_generate_pdf_extension():

    pdf_path = generate_pdf(

        filename="report_test.pdf",

        participant="Usuario Test",

        email="usuario@test.com",

        age=25,

        gender="Masculino",

        score=15,

        risk="Moderado",

        evaluation_id=999

    )

    assert pdf_path.endswith(".pdf")

def test_generate_pdf_not_empty():

    pdf_path = generate_pdf(

        filename="report_test.pdf",

        participant="Usuario Test",

        email="usuario@test.com",

        age=25,

        gender="Masculino",

        score=15,

        risk="Moderado",

        evaluation_id=999

    )

    size = Path(pdf_path).stat().st_size

    assert size > 0

def test_generate_pdf_returns_string():

    pdf_path = generate_pdf(

        filename="report_test.pdf",

        participant="Usuario Test",

        email="usuario@test.com",

        age=25,

        gender="Masculino",

        score=15,

        risk="Moderado",

        evaluation_id=999

    )

    assert isinstance(pdf_path, str)