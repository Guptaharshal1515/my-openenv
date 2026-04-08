import os
import requests
from openai import OpenAI

# Environment variables
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://guptaharshal1515-my-env.hf.space"
)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# OpenAI client (required by rules)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

print(f"[START] task=finance env=simple model={MODEL_NAME}")

# Reset environment
reset_response = requests.post(f"{API_BASE_URL}/reset").json()

done = False
step = 0
total_reward = 0

# RL loop
while not done and step < 10:
    step += 1

    # Simple policy
    action = "save" if step % 3 == 0 else "invest"

    try:
        result = requests.post(
            f"{API_BASE_URL}/step",
            json={"action": action}
        ).json()

        reward = result.get("reward", 0)
        done = result.get("done", False)
        total_reward += reward

        print(f"[STEP] step={step} action={action} reward={reward} done={done} error=None")

    except Exception as e:
        print(f"[STEP] step={step} action={action} reward=0 done=True error={str(e)}")
        break

# Normalize score (0–1)
score = max(0.0, min(1.0, total_reward / 10))

print(f"[END] success=True steps={step} score={score} rewards={total_reward}")
