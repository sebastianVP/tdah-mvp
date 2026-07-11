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

    Si el correo ya existe, devuelve el ID del participante existente.

    Si el correo no existe, crea un nuevo participante.

    Si db=None, crea su propia sesión (uso normal desde Streamlit).

    Si recibe una sesión, utiliza esa sesión (uso en pruebas).
    """

    own_session = False

    if db is None:

        db = SessionLocal()

        own_session = True

    try:
        # ==========================================================
        # Verificar si el participante ya existe
        # ==========================================================

        participant = (
            db.query(Participant)
            .filter(Participant.email == email)
            .first()
        )

        if participant:

            return participant.id

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