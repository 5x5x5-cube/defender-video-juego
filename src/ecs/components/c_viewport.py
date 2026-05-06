from src.ecs.components.c_player_state import FacingDirection


class CViewport:
    def __init__(self, world_width: float, screen_width: float) -> None:
        self.origin_x = 0.0
        self.world_width = world_width
        self.screen_width = screen_width
        self.last_facing = FacingDirection.RIGHT
        self.transition_timer = 0.0
        self.in_transition = False

    def world_to_screen_x(self, entity_x: float) -> float:
        diff = entity_x - self.origin_x
        if self.world_width > 0:
            half_world = self.world_width / 2
            if diff < -half_world:
                diff += self.world_width
            elif diff > half_world:
                diff -= self.world_width
        return diff
