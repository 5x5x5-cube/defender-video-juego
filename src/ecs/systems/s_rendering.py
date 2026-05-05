import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_viewport import CViewport


def system_rendering(world: esper.World, screen: pygame.Surface):
    viewport_origin_x = _get_viewport_origin_x(world)
    screen_rect = screen.get_rect()
    for _, (c_transform, c_surface) in world.get_components(CTransform, CSurface):
        draw_x = c_transform.pos.x - viewport_origin_x
        draw_y = c_transform.pos.y
        if draw_x + c_surface.area.width < 0 or draw_x > screen_rect.width:
            continue
        screen.blit(c_surface.surf, (draw_x, draw_y), c_surface.area)


def _get_viewport_origin_x(world: esper.World) -> float:
    for _, c_viewport in world.get_component(CViewport):
        return c_viewport.origin_x
    return 0.0
