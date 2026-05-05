import esper
import pygame

from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_player import CTagPlayer

_font = None
_COLOR = pygame.Color(0, 255, 0)
_BG_COLOR = pygame.Color(0, 0, 0, 180)
_LINE_HEIGHT = 10
_PADDING = 4


def system_debug_rendering(world: esper.World, screen: pygame.Surface):
    global _font
    if _font is None:
        _font = pygame.font.SysFont("monospace", 10)

    lines = _collect_debug_info(world)
    _draw_debug_panel(screen, lines)


def _collect_debug_info(world: esper.World) -> list[str]:
    lines = []

    for _, (c_transform, c_velocity, c_player_state, _) in world.get_components(
            CTransform, CVelocity, CPlayerState, CTagPlayer):
        lines.append(f"pos: ({c_transform.pos.x:.0f}, {c_transform.pos.y:.0f})")
        lines.append(f"vel: ({c_velocity.vel.x:.1f}, {c_velocity.vel.y:.1f})")
        lines.append(f"speed: {abs(c_velocity.vel.x):.1f}")
        lines.append(f"facing: {c_player_state.facing.name}")
        lines.append(f"moving: {c_player_state.moving_horizontal}")

    for _, c_viewport in world.get_component(CViewport):
        lines.append(f"cam: {c_viewport.origin_x:.0f}")

    return lines


def _draw_debug_panel(screen: pygame.Surface, lines: list[str]):
    if not lines:
        return

    panel_width = max(len(line) for line in lines) * 7 + _PADDING * 2
    panel_height = len(lines) * _LINE_HEIGHT + _PADDING * 2
    panel_x = screen.get_width() - panel_width - _PADDING
    panel_y = _PADDING

    panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel_surface.fill(_BG_COLOR)
    screen.blit(panel_surface, (panel_x, panel_y))

    for i, line in enumerate(lines):
        text_surface = _font.render(line, False, _COLOR)
        screen.blit(text_surface, (panel_x + _PADDING,
                                   panel_y + _PADDING + i * _LINE_HEIGHT))
