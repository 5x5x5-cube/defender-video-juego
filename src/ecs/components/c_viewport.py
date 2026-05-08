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
        return self.to_screen_x(entity_x, 1.0)

    def to_screen_x(self, entity_x: float, parallax_factor: float) -> float:
        effective_origin = self.origin_x * parallax_factor
        effective_world_width = self.world_width * parallax_factor
        diff = entity_x - effective_origin
        if effective_world_width > 0:
            half = effective_world_width / 2
            if diff < -half:
                diff += effective_world_width
            elif diff > half:
                diff -= effective_world_width
        return diff
