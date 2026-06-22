from app.database.db import SessionLocal
from app.database.models import Evaluation


def save_evaluation(
    participant_id: int,
    score: int,
    risk_level: str,
    responses: list
):
    
    db = SessionLocal()

    try:

        evaluation = Evaluation(
            participant_id=participant_id,
            score=score,
            max_score=72,
            probability_level=risk_level,
            responses=responses
        )

        db.add(evaluation)

        db.commit()

        db.refresh(evaluation)

        return evaluation.id

    except Exception as e:

        print("ERROR:", e)

        raise

    finally:
        db.close()