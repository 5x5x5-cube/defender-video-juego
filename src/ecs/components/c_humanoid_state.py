from enum import Enum


class HumanoidState(Enum):
    ON_GROUND = 0
    CAPTURED = 1
    FALLING = 2


class CHumanoidState:
    def __init__(self, spawn_x: float, spawn_y: float) -> None:
        self.state = HumanoidState.ON_GROUND
        self.spawn_x = spawn_x
        self.spawn_y = spawn_y
        self.fall_start_y: float = 0.0
