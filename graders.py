def grade_easy(state):
    balance = state["balance"]
    score = balance / 2000
    return max(0.01, min(0.99, score))


def grade_medium(state):
    balance = state["balance"]
    score = balance / 1800
    return max(0.01, min(0.99, score))


def grade_hard(state):
    balance = state["balance"]
    score = balance / 1500
    return max(0.01, min(0.99, score))
