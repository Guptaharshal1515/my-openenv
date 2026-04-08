from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from server.environment import SimpleEnv

app = FastAPI()
env = SimpleEnv()


class StepRequest(BaseModel):
    action: str


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/reset")
def reset():
    obs = env.reset()
    return {
        "observation": obs,
        "reward": 0.0,
        "done": False
    }


@app.get("/reset")
def reset_get():
    return reset()


@app.post("/step")
def step(req: StepRequest):
    try:
        obs, reward, done = env.step(req.action)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "observation": obs,
        "reward": reward,
        "done": done
    }


@app.get("/state")
def state():
    return env.get_state()


def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()
