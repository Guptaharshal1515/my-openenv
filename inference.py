import os
import requests
from openai import OpenAI

API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
SERVER_URL = os.getenv("SERVER_URL", "http://localhost:7860")

client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)


def call_env(method, endpoint, payload=None):
    url = f"{SERVER_URL}{endpoint}"
    if method == "POST":
        response = requests.post(url, json=payload, timeout=20)
    else:
        response = requests.get(url, timeout=20)
    response.raise_for_status()
    return response.json()


def choose_action(observation):
    prompt = (
        "You are choosing one action for a simple finance environment. "
        f"Current state: {observation}. "
        "Return exactly one token from: save, spend, invest."
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    action = (response.choices[0].message.content or "").strip().lower()
    if action not in {"save", "spend", "invest"}:
        action = "save"
    return action


def main():
    print(f"[START] task=finance env=simple model={MODEL_NAME}")

    steps = 0
    total_reward = 0.0
    done = False
    score = 0

    try:
        reset_result = call_env("POST", "/reset")
        observation = reset_result["observation"]

        while not done and steps < 10:
            steps += 1
            action = choose_action(observation)
            error = None

            try:
                step_result = call_env("POST", "/step", {"action": action})
                observation = step_result["observation"]
                reward = float(step_result["reward"])
                done = bool(step_result["done"])
                score = int(observation.get("balance", 0))
                total_reward += reward
                print(
                    f"[STEP] step={steps} action={action} reward={reward} done={done} error={error}"
                )
            except Exception as exc:
                reward = 0.0
                done = False
                error = str(exc)
                print(
                    f"[STEP] step={steps} action={action} reward={reward} done={done} error={error}"
                )
                break

        success = done
        print(
            f"[END] success={success} steps={steps} score={score} rewards={total_reward}"
        )

    except Exception as exc:
        print(f"[STEP] step=1 action=save reward=0.0 done=False error={exc}")
        print("[END] success=False steps=0 score=0 rewards=0.0")


if __name__ == "__main__":
    main()
