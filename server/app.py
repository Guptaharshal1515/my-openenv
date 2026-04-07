from fastapi import FastAPI
from server.environment import SimpleEnv

app = FastAPI()
env = SimpleEnv()

@app.get("/health")
def health():
    return {"status": "healthy"}


# POST reset (main one)
@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs,
        "reward": 0,
        "done": False
    }


# GET reset (for browser testing)
@app.get("/reset")
def reset_get():
    return reset()


@app.post("/step")
def step(action: dict):
    obs, reward, done = env.step(action.get("action", "save"))
    return {
        "observation": obs,
        "reward": reward,
        "done": done
    }
