from enum import Enum


class LanderState(Enum):
    WANDER = 0
    HUNTING = 1
    CAPTURE = 2


class CEnemyLanderState:
    def __init__(self) -> None:
        self.state = LanderState.WANDER
        self.target_humanoid = -1
