from app.services.participant_service import save_participant

from app.services.evaluation_service import save_evaluation


def test_save_evaluation_returns_id(db_session):

    participant_id = save_participant(

        full_name="Usuario Evaluacion",

        email="evaluacion001@example.com",

        age=30,

        gender="Masculino",

        db = db_session

    )

    evaluation_id = save_evaluation(

        participant_id=participant_id,

        score=18,

        risk_level="Alto",

        responses=[

            "Muy frecuentemente"

        ] * 18,

        db=db_session

    )

    assert evaluation_id is not None

def test_save_evaluation_returns_integer(db_session):

    participant_id = save_participant(

        full_name="Usuario Evaluacion 2",

        email="evaluacion002@example.com",

        age=28,

        gender="Femenino",

        db= db_session

    )

    evaluation_id = save_evaluation(

        participant_id=participant_id,

        score=12,

        risk_level="Moderado",

        responses=[

            "Algunas veces"

        ] * 18,

        db =db_session

    )

    assert isinstance(

        evaluation_id,

        int

    )

def test_save_evaluation_positive_id(db_session):

    participant_id = save_participant(

        full_name="Usuario Evaluacion 3",

        email="evaluacion003@example.com",

        age=40,

        gender="Otro",

        db= db_session

    )

    evaluation_id = save_evaluation(

        participant_id=participant_id,

        score=5,

        risk_level="Bajo",

        responses=[

            "Nunca"

        ] * 18,

        db = db_session

    )

    assert evaluation_id > 0