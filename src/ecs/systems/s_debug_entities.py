import esper
import pygame

from src.ecs.components.c_parallax import CParallax, get_world_position
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_humanoid import CTagHumanoid

_font = None
_COLOR_ENEMY = pygame.Color(255, 100, 100)
_COLOR_HUMANOID = pygame.Color(100, 255, 100)
_BG_COLOR = pygame.Color(0, 0, 0, 180)
_LINE_HEIGHT = 8
_PADDING = 2


def system_debug_entities(world: esper.World, screen: pygame.Surface, hud_height: int):
    global _font
    if _font is None:
        _font = pygame.font.SysFont("monospace", 8)

    viewport_data = _get_viewport_data(world)
    if viewport_data is None:
        return

    c_viewport = viewport_data

    for entity, (c_transform, c_surface, _) in world.get_components(
            CTransform, CSurface, CTagEnemy):
        _draw_entity_debug(world, screen, entity, c_transform, c_surface,
                           c_viewport, hud_height, _COLOR_ENEMY, "E")

    for entity, (c_transform, c_surface, _) in world.get_components(
            CTransform, CSurface, CTagHumanoid):
        _draw_entity_debug(world, screen, entity, c_transform, c_surface,
                           c_viewport, hud_height, _COLOR_HUMANOID, "H")


def _get_viewport_data(world: esper.World):
    for _, c_viewport in world.get_component(CViewport):
        return c_viewport
    return None


def _draw_entity_debug(world: esper.World, screen: pygame.Surface,
                       entity: int, c_transform: CTransform,
                       c_surface: CSurface, c_viewport: CViewport,
                       hud_height: int, color: pygame.Color, label: str):
    parallax_factor = 1.0
    if world.has_component(entity, CParallax):
        parallax_factor = world.component_for_entity(entity, CParallax).factor

    world_pos = get_world_position(world, entity, c_transform)
    screen_x = c_viewport.to_screen_x(c_transform.pos.x, parallax_factor)

    lines = [
        f"{label} w:({world_pos.x:.0f},{world_pos.y:.0f})",
        f"  p:({c_transform.pos.x:.0f},{c_transform.pos.y:.0f})",
        f"  f:{parallax_factor}",
    ]

    panel_width = max(len(line) for line in lines) * 5 + _PADDING * 2
    panel_height = len(lines) * _LINE_HEIGHT + _PADDING * 2
    panel_x = int(screen_x + c_surface.area.width + 2)
    panel_y = int(c_transform.pos.y + hud_height - 4)

    if panel_x + panel_width > screen.get_width():
        panel_x = int(screen_x - panel_width - 2)

    panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel_surface.fill(_BG_COLOR)
    screen.blit(panel_surface, (panel_x, panel_y))

    for i, line in enumerate(lines):
        text_surface = _font.render(line, False, color)
        screen.blit(text_surface, (panel_x + _PADDING,
                                   panel_y + _PADDING + i * _LINE_HEIGHT))
