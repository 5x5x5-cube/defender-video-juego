import random


class CShootTimer:
    def __init__(self, cooldown_min: float, cooldown_max: float) -> None:
        self.cooldown_min = cooldown_min
        self.cooldown_max = cooldown_max
        self.timer = random.uniform(cooldown_min, cooldown_max)

    def reset(self):
        self.timer = random.uniform(self.cooldown_min, self.cooldown_max)

    def disable(self):
        self.timer = float('inf')
