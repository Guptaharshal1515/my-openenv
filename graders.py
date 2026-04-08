


def clamp_score(score):
    # Clamp to strictly (0, 1)
    if score <= 0:
        return 0.0001
    elif score >= 1:
        return 0.9999
    return score

def grade_easy(states, rewards):
    # Example: accuracy = percent of steps with balance >= 900
    correct = sum(1 for s in states if s["balance"] >= 900)
    accuracy = correct / len(states) if states else 0
    avg_reward = sum(rewards) / len(rewards) if rewards else 0
    score = (accuracy + avg_reward) / 2
    return {"score": clamp_score(score), "accuracy": clamp_score(accuracy), "avg_reward": clamp_score(avg_reward)}

def grade_medium(states, rewards):
    correct = sum(1 for s in states if s["balance"] >= 1100)
    accuracy = correct / len(states) if states else 0
    avg_reward = sum(rewards) / len(rewards) if rewards else 0
    score = (accuracy + avg_reward) / 2
    return {"score": clamp_score(score), "accuracy": clamp_score(accuracy), "avg_reward": clamp_score(avg_reward)}

def grade_hard(states, rewards):
    # Use normalized final balance as score
    final_balance = states[-1]["balance"] if states else 0
    score = final_balance / 1500
    avg_reward = sum(rewards) / len(rewards) if rewards else 0
    return {"score": clamp_score(score), "avg_reward": clamp_score(avg_reward)}
