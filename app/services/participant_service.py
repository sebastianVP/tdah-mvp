from app.database.db import SessionLocal
from app.database.models import Participant

def save_participant(
        full_name,
        email,
        age,
        gender
):
    db = SessionLocal()
    
    try:
        # 1. Buscar si ya existe
        existing = db.query(Participant).filter(
            Participant.email == email
        ).first()

        if existing:
            return existing.id  # reutiliza el usuario

        participant= Participant(
            full_name = full_name,
            email     = email,
            age       = age,
            gender    = gender,
            consent   = True
        )

        db.add(participant)
        
        db.commit()

        db.refresh(participant)

        return participant.id
    finally:
        db.close()
