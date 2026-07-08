from app.database.db import SessionLocal
from app.database.models import Participant


def save_participant(
    full_name,
    email,
    age,
    gender,
    db=None
):
    """
    Guarda un participante.

    Si db=None, crea su propia sesión (uso normal desde Streamlit).

    Si recibe una sesión, utiliza esa sesión (uso en pruebas).
    """

    own_session = False

    if db is None:

        db = SessionLocal()

        own_session = True

    try:

        participant = Participant(

            full_name=full_name,

            email=email,

            age=age,

            gender=gender,

            consent=True

        )

        db.add(participant)

        # Solo hacemos commit cuando la sesión es propia
        if own_session:

            db.commit()

        else:

            db.flush()

        db.refresh(participant)

        return participant.id

    finally:

        if own_session:

            db.close()