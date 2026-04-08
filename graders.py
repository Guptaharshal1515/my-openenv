EPSILON = 1e-6


def _strict_unit_interval(value: float) -> float:
    """Clamp a score so it is strictly inside (0, 1)."""
    return min(1.0 - EPSILON, max(EPSILON, float(value)))


def grade_easy(state):
    raw = 1.0 if state["balance"] >= 900 else 0.0
    return _strict_unit_interval(raw)


def grade_medium(state):
    raw = 1.0 if state["balance"] >= 1100 else 0.0
    return _strict_unit_interval(raw)


def grade_hard(state):
    score = state["balance"] / 1500
    return _strict_unit_interval(score)
