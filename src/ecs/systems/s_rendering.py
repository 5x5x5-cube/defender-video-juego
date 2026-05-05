import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_viewport import CViewport


def system_rendering(world: esper.World, screen: pygame.Surface):
    viewport_origin_x, world_width = _get_viewport_data(world)
    screen_rect = screen.get_rect()
    for _, (c_transform, c_surface) in world.get_components(CTransform, CSurface):
        draw_x = _screen_position_in_circular_world(
            c_transform.pos.x, viewport_origin_x, world_width)
        draw_y = c_transform.pos.y
        if draw_x + c_surface.area.width < 0 or draw_x > screen_rect.width:
            continue
        screen.blit(c_surface.surf, (draw_x, draw_y), c_surface.area)


def _get_viewport_data(world: esper.World) -> tuple[float, float]:
    for _, c_viewport in world.get_component(CViewport):
        return c_viewport.origin_x, c_viewport.world_width
    return 0.0, 0.0


def _screen_position_in_circular_world(entity_x: float, viewport_origin_x: float,
                        world_width: float) -> float:
    draw_x = entity_x - viewport_origin_x
    if world_width > 0:
        half_world = world_width / 2
        if draw_x < -half_world:
            draw_x += world_width
        elif draw_x > half_world:
            draw_x -= world_width
    return draw_x
