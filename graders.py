def clamp(score):
    return max(0.01, min(0.99, score))


def grade_easy(state):
    score = 1.0 if state["balance"] >= 900 else 0.0
    return clamp(score)


def grade_medium(state):
    score = 1.0 if state["balance"] >= 1100 else 0.0
    return clamp(score)


def grade_hard(state):
    score = state["balance"] / 1500
    return clamp(score)
