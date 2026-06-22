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
