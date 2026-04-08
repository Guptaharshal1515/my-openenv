START_BALANCE = 1000.0
MAX_BALANCE = 2000.0
MIN_SCORE = 0.01
MAX_SCORE = 0.99


def _clamp_score(score: float) -> float:
    """Clamp final score strictly inside (0, 1)."""
    return max(MIN_SCORE, min(MAX_SCORE, float(score)))


def _balance_component(balance: float) -> float:
    """Normalize balance to [0, 1] using the required 0..2000 range."""
    normalized = balance / MAX_BALANCE
    return max(0.0, min(1.0, normalized))


def _stability_component(balance: float) -> float:
    """Higher when balance stays above the start value; smooth penalty below start."""
    if balance >= START_BALANCE:
        # Mild reward for staying above start, capped at 1.0.
        return min(1.0, 0.75 + ((balance - START_BALANCE) / START_BALANCE) * 0.25)

    # Stronger penalty as losses deepen; 0 at zero balance.
    return max(0.0, balance / START_BALANCE)


def _efficiency_component(balance: float, step_count: int) -> float:
    """Reward more gain in fewer steps with smooth diminishing returns."""
    steps = max(1, int(step_count))
    gain = max(0.0, balance - START_BALANCE)
    gain_ratio = gain / START_BALANCE
    # Scale by steps so similar gains in fewer steps score better.
    return max(0.0, min(1.0, gain_ratio * (10.0 / steps)))


def grade_easy(state):
    balance = float(state.get("balance", 0))

    # EASY: mostly final balance using required 0..2000 normalization.
    balance_score = _balance_component(balance)
    score = 0.9 * balance_score + 0.1 * 0.5

    return _clamp_score(score)


def grade_medium(state):
    balance = float(state.get("balance", 0))

    # MEDIUM: combine balance + stability; low balance is naturally penalized.
    balance_score = _balance_component(balance)
    stability_score = _stability_component(balance)

    score = 0.65 * balance_score + 0.35 * stability_score
    return _clamp_score(score)


def grade_hard(state):
    balance = float(state.get("balance", 0))
    step_count = int(state.get("step_count", 0))

    # HARD: balance + stability + efficiency with extra penalty for high step count.
    balance_score = _balance_component(balance)
    stability_score = _stability_component(balance)
    efficiency_score = _efficiency_component(balance, step_count)

    # Extra smooth penalty if episode runs too long.
    extra_step_penalty = max(0.0, (step_count - 8) * 0.02)

    score = (
        0.5 * balance_score
        + 0.25 * stability_score
        + 0.25 * efficiency_score
        - extra_step_penalty
    )

    return _clamp_score(score)
