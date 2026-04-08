LOWER_BOUND = 0.001
UPPER_BOUND = 0.999


def _strict_unit_interval(value: float) -> float:
    """Clamp a score so it is strictly inside (0, 1)."""
    return min(UPPER_BOUND, max(LOWER_BOUND, float(value)))


def grade_easy(state):
    balance = state.get("balance", 0)
    # Linear score around easy target so output is never binary 0/1.
    raw = balance / 1200.0
    return _strict_unit_interval(raw)


def grade_medium(state):
    balance = state.get("balance", 0)
    # Slightly stricter normalization than easy.
    raw = balance / 1400.0
    return _strict_unit_interval(raw)


def grade_hard(state):
    balance = state.get("balance", 0)
    # Hard task uses the most demanding target.
    score = balance / 1600.0
    return _strict_unit_interval(score)
