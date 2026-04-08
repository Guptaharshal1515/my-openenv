class SimpleEnv:
    def __init__(self):
        self.balance = 1000
        self.step_count = 0

    def reset(self):
        self.balance = 1000
        self.step_count = 0
        return {"balance": self.balance, "step_count": self.step_count}

    def step(self, action: str):
        old_balance = self.balance
        next_step = self.step_count + 1

        if action == "save":
            self.balance += 50
        elif action == "spend":
            self.balance -= 50
        elif action == "invest":
            # deterministic: even step = gain, odd = loss
            if next_step % 2 == 0:
                self.balance += 100
            else:
                self.balance -= 100
        else:
            raise ValueError("Invalid action. Use save, spend, or invest")

        self.step_count = next_step

        reward = (self.balance - old_balance) / 100
        done = self.step_count >= 10

        return {"balance": self.balance, "step_count": self.step_count}, reward, done

    
    def get_state(self):
        return {
            "balance": self.balance,
            "step_count": self.step_count
        }
