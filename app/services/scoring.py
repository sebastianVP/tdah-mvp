SCORES = {
    "Nunca": 0,
    "Rara vez": 1,
    "Algunas veces": 2,
    "Frecuentemente": 3,
    "Muy frecuentemente": 4,
}

def calculate_score(responses):
    return sum(SCORES[r] for r in responses)