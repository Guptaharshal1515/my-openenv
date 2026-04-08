

def grade_easy(state):
    # Always strictly between 0 and 1
    if state["balance"] >= 900:
        return 0.9999
    else:
        return 0.0001

def grade_medium(state):
    # Always strictly between 0 and 1
    if state["balance"] >= 1100:
        return 0.9999
    else:
        return 0.0001

def grade_hard(state):
    # Always strictly between 0 and 1
    score = state["balance"] / 1500
    if score <= 0:
        return 0.0001
    elif score >= 1:
        return 0.9999
    return score
