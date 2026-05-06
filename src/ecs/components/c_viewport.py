from src.ecs.components.c_player_state import FacingDirection


class CViewport:
    def __init__(self, world_width: float, screen_width: float) -> None:
        self.origin_x = 0.0
        self.world_width = world_width
        self.screen_width = screen_width
        self.last_facing = FacingDirection.RIGHT
        self.transition_timer = 0.0
        self.in_transition = False
