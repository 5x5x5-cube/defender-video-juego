from enum import Enum


class FacingDirection(Enum):
    RIGHT = 1
    LEFT = -1


class VerticalDirection(Enum):
    NONE = 0
    UP = -1
    DOWN = 1


class CPlayerState:
    def __init__(self) -> None:
        self.facing = FacingDirection.RIGHT
        self.moving_horizontal = False
        self.vertical = VerticalDirection.NONE
