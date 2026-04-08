import os
import requests
from openai import OpenAI

# Environment variables
API_BASE_URL = os.getenv("API_BASE_URL")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
API_KEY = os.getenv("API_KEY")

# OpenAI client (required by rules)
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
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


    from openai import OpenAI
    import os
    import requests

    API_BASE_URL = os.getenv("API_BASE_URL")
    API_KEY = os.getenv("API_KEY")
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    SERVER_URL = os.getenv("SERVER_URL", "http://localhost:7860")

    def call_api(method, endpoint, **kwargs):
        url = f"{SERVER_URL}{endpoint}"
        try:
            if method == "post":
                r = requests.post(url, json=kwargs.get("json"))
            else:
                r = requests.get(url)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            return None

    def choose_action_llm(observation):
        prompt = f"Given the state {observation}, choose one action: save, spend, or invest. Only reply with the action."
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            action = response.choices[0].message.content.strip().lower()
            if action not in ["save", "spend", "invest"]:
                action = "save"
            return action
        except Exception:
            return "save"

    def main():
        model = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
        print(f"[START] task=finance env=simple model={model}")

        resp = call_api("post", "/reset")
        if not resp:
            print(f"[STEP] step=0 action=reset reward=0 done=False error=reset_failed")
            print(f"[END] success=False steps=0 score=0 rewards=0")
            return

        obs = resp["observation"]
        reward = resp["reward"]
        done = resp["done"]
        total_reward = 0
        steps = 0

        for step in range(1, 11):
            action = choose_action_llm(obs)
            resp = call_api("post", "/step", json={"action": action})
            if not resp or "error" in resp:
                print(f"[STEP] step={step} action={action} reward=0 done=False error={resp.get('error') if resp else 'step_failed'}")
                break
            reward = resp["reward"]
            done = resp["done"]
            obs = resp["observation"]
            total_reward += reward
            print(f"[STEP] step={step} action={action} reward={reward} done={done} error=None")
            steps += 1
            if done:
                break

        print(f"[END] success={done} steps={steps} score={obs['balance']} rewards={total_reward}")

    if __name__ == "__main__":
        main()
