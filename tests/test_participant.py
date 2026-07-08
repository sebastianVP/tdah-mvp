from app.services.participant_service import save_participant


def test_save_participant_returns_id(db_session):

    participant_id = save_participant(

        full_name="Usuario Test",

        email="usuario_test_001@example.com",

        age=25,

        gender="Masculino",
        
        db=db_session

    )

    assert participant_id is not None

def test_save_participant_returns_integer(db_session):

    participant_id = save_participant(

        full_name="Usuario Test 2",

        email="usuario_test_002@example.com",

        age=30,

        gender="Femenino",

        db=db_session

    )

    assert isinstance(
        participant_id,
        int
    )

def test_save_participant_positive_id(db_session):

    participant_id = save_participant(

        full_name="Usuario Test 3",

        email="usuario_test_003@example.com",

        age=40,

        gender="Otro",

        db=db_session

    )

    assert participant_id > 0