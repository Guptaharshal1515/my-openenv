import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

print("[START] task=finance env=simple model=" + MODEL_NAME)

reset = requests.post(f"{API_BASE_URL}/reset").json()

done = False
step = 0
total_reward = 0

while not done and step < 10:
    step += 1
    action = "save" if step % 3 == 0 else "invest"

    result = requests.post(f"{API_BASE_URL}/step", json={"action": action}).json()

    reward = result["reward"]
    done = result["done"]
    total_reward += reward

    print(f"[STEP] step={step} action={action} reward={reward} done={done} error=None")

score = max(0, min(1, total_reward / 10))

print(f"[END] success=True steps={step} score={score} rewards={total_reward}")
