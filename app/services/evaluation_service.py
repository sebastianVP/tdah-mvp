from app.database.db import SessionLocal
from app.database.models import Evaluation


def save_evaluation(
    participant_id,
    score,
    risk_level,
    responses,
    db=None
):

    own_session = False

    if db is None:

        db = SessionLocal()

        own_session = True

    try:

        evaluation = Evaluation(

            participant_id=participant_id,

            score=score,

            max_score=72,

            probability_level=risk_level,

            responses=responses

        )

        db.add(evaluation)

        if own_session:

            db.commit()

        else:

            db.flush()

        db.refresh(evaluation)

        return evaluation.id

    finally:

        if own_session:

            db.close()