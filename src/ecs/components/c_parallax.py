import esper
import pygame


class CParallax:
    def __init__(self, factor: float) -> None:
        self.factor = factor

    def to_world_x(self, parallax_x: float) -> float:
        return parallax_x / self.factor if self.factor != 0 else parallax_x

    def to_parallax_x(self, world_x: float) -> float:
        return world_x * self.factor


def get_world_position(world: esper.World, entity: int,
                       c_transform) -> pygame.Vector2:
    if world.has_component(entity, CParallax):
        c_parallax = world.component_for_entity(entity, CParallax)
        return pygame.Vector2(
            c_parallax.to_world_x(c_transform.pos.x),
            c_transform.pos.y
        )
    return c_transform.pos.copy()
