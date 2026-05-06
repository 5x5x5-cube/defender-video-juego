import esper
import pygame

from src.ecs.components.c_parallax import CParallax
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_viewport import CViewport


def system_rendering(world: esper.World, screen: pygame.Surface):
    viewport_origin_x, world_width = _get_viewport_data(world)
    screen_rect = screen.get_rect()
    for entity, (c_transform, c_surface) in world.get_components(CTransform, CSurface):
        parallax_factor = _get_parallax_factor(world, entity)
        effective_origin = viewport_origin_x * parallax_factor
        effective_world_width = world_width * parallax_factor
        draw_y = c_transform.pos.y

        for draw_x in _get_draw_positions(c_transform, c_surface,
                                          effective_origin, effective_world_width):
            if _is_off_screen(draw_x, c_surface, screen_rect):
                continue
            screen.blit(c_surface.surf, (draw_x, draw_y), c_surface.area)


def _get_viewport_data(world: esper.World) -> tuple[float, float]:
    for _, c_viewport in world.get_component(CViewport):
        return c_viewport.origin_x, c_viewport.world_width
    return 0.0, 0.0


def _get_parallax_factor(world: esper.World, entity: int) -> float:
    if world.has_component(entity, CParallax):
        return world.component_for_entity(entity, CParallax).factor
    return 1.0


def _get_draw_positions(c_transform: CTransform, c_surface: CSurface,
                        effective_origin: float,
                        effective_world_width: float) -> list[float]:
    if effective_world_width <= 0:
        return [c_transform.pos.x - effective_origin]

    if _spans_world(c_surface, effective_world_width):
        draw_x = (c_transform.pos.x - effective_origin) % effective_world_width
        return [draw_x - effective_world_width, draw_x]

    draw_x = c_transform.pos.x - effective_origin
    draw_x = draw_x % effective_world_width
    if draw_x > effective_world_width / 2:
        draw_x -= effective_world_width
    return [draw_x]


def _spans_world(c_surface: CSurface, effective_world_width: float) -> bool:
    return c_surface.surf.get_width() > effective_world_width / 2


def _is_off_screen(draw_x: float, c_surface: CSurface,
                   screen_rect: pygame.Rect) -> bool:
    return draw_x + c_surface.area.width < 0 or draw_x > screen_rect.width
