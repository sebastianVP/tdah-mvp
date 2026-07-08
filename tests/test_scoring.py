from app.services.scoring import calculate_score


def test_score_all_zero():

    responses = [
        "Nunca"
    ] * 18

    score = calculate_score(
        responses
    )

    assert score == 0

def test_score_maximum():

    responses = [
        "Muy frecuentemente"
    ] * 18

    score = calculate_score(
        responses
    )

    assert score == 72

def test_score_returns_integer():

    responses = [
        "Algunas veces"
    ] * 18

    score = calculate_score(
        responses
    )

    assert isinstance(
        score,
        int
    )