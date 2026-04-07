class SimpleEnv:
    def __init__(self):
        self.balance = 1000
        self.step_count = 0

    def reset(self):
        self.balance = 1000
        self.step_count = 0
        return {"balance": self.balance}

    def step(self, action: str):
        self.step_count += 1
        old_balance = self.balance

        if action == "save":
            self.balance += 50
        elif action == "spend":
            self.balance -= 50
        elif action == "invest":
            # deterministic: even step = gain, odd = loss
            if self.step_count % 2 == 0:
                self.balance += 100
            else:
                self.balance -= 100

        reward = (self.balance - old_balance) / 100
        done = self.step_count >= 10

        return {"balance": self.balance}, reward, done
