
def grade_easy(state):
    score = 1.0 if state["balance"] >= 900 else 0.0001
    return score if score < 1.0 else 0.9999

def grade_medium(state):
    score = 1.0 if state["balance"] >= 1100 else 0.0001
    return score if score < 1.0 else 0.9999

def grade_hard(state):
    score = state["balance"] / 1500
    if score <= 0:
        return 0.0001
    elif score >= 1:
        return 0.9999
    return score
