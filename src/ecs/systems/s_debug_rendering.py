import esper
import pygame

from src.ecs.components.c_player_state import CPlayerState, FacingDirection
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_player import CTagPlayer

_font = None
_COLOR = pygame.Color(0, 255, 0)
_BG_COLOR = pygame.Color(0, 0, 0, 180)
_LINE_HEIGHT = 10
_PADDING = 4


def system_debug_rendering(world: esper.World, screen: pygame.Surface,
                           hud_height: int = 0):
    global _font
    if _font is None:
        _font = pygame.font.SysFont("monospace", 10)

    player_data = _get_player_data(world)
    c_viewport = _get_viewport(world)

    if c_viewport is not None:
        _draw_viewport_border(screen, hud_height)
        _draw_corner_coordinates(screen, c_viewport, hud_height)
        if player_data is not None:
            _draw_ship_position_indicator(screen, player_data, c_viewport, hud_height)
            _draw_camera_info(screen, player_data, c_viewport)

    if player_data is not None:
        _draw_ship_info_card(screen, player_data, c_viewport, hud_height)


def _get_player_data(world: esper.World):
    for _, (c_transform, c_velocity, c_player_state, _) in world.get_components(
            CTransform, CVelocity, CPlayerState, CTagPlayer):
        return c_transform, c_velocity, c_player_state
    return None


def _get_viewport(world: esper.World):
    for _, c_viewport in world.get_component(CViewport):
        return c_viewport
    return None


def _draw_viewport_border(screen: pygame.Surface, hud_height: int):
    screen_w = screen.get_width()
    screen_h = screen.get_height()
    pygame.draw.rect(screen, _COLOR,
                     (0, hud_height, screen_w, screen_h - hud_height), 1)


def _draw_corner_coordinates(screen: pygame.Surface, c_viewport: CViewport,
                             hud_height: int):
    screen_w = screen.get_width()
    screen_h = screen.get_height()
    origin = c_viewport.origin_x
    right_edge = origin + c_viewport.screen_width
    if c_viewport.world_width > 0:
        right_edge = right_edge % c_viewport.world_width

    tl_text = _font.render(f"{origin:.0f}", False, _COLOR)
    screen.blit(tl_text, (2, hud_height + 2))

    tr_text = _font.render(f"{right_edge:.0f}", False, _COLOR)
    screen.blit(tr_text, (screen_w - tr_text.get_width() - 2, hud_height + 2))

    bl_text = _font.render(f"{origin:.0f}", False, _COLOR)
    screen.blit(bl_text, (2, screen_h - bl_text.get_height() - 2))

    br_text = _font.render(f"{right_edge:.0f}", False, _COLOR)
    screen.blit(br_text, (screen_w - br_text.get_width() - 2,
                          screen_h - br_text.get_height() - 2))


def _draw_ship_position_indicator(screen: pygame.Surface, player_data,
                                  c_viewport: CViewport, hud_height: int):
    c_transform, _, _ = player_data
    screen_x = c_viewport.world_to_screen_x(c_transform.pos.x)
    ratio = screen_x / c_viewport.screen_width if c_viewport.screen_width > 0 else 0
    indicator_x = int(ratio * screen.get_width())
    indicator_x = max(0, min(screen.get_width() - 1, indicator_x))

    marker_h = 6
    pygame.draw.rect(screen, pygame.Color(255, 255, 0),
                     (indicator_x - 2, hud_height, 5, marker_h))

    pct_text = _font.render(f"{ratio * 100:.0f}%", False, pygame.Color(255, 255, 0))
    text_x = max(0, min(indicator_x - pct_text.get_width() // 2,
                        screen.get_width() - pct_text.get_width()))
    screen.blit(pct_text, (text_x, hud_height + marker_h + 1))


def _draw_ship_info_card(screen: pygame.Surface, player_data,
                         c_viewport, hud_height: int):
    c_transform, c_velocity, c_player_state = player_data

    lines = [
        f"pos:({c_transform.pos.x:.0f},{c_transform.pos.y:.0f})",
        f"vel:({c_velocity.vel.x:.0f},{c_velocity.vel.y:.0f})",
        f"spd:{abs(c_velocity.vel.x):.0f}",
        f"dir:{c_player_state.facing.name}",
    ]

    screen_x = c_viewport.world_to_screen_x(c_transform.pos.x) if c_viewport else c_transform.pos.x
    card_x = int(screen_x) + 20
    card_y = int(c_transform.pos.y) + hud_height - 20

    _draw_info_card(screen, lines, card_x, card_y, _COLOR)


def _draw_camera_info(screen: pygame.Surface, player_data, c_viewport: CViewport):
    c_transform, _, c_player_state = player_data
    player_x = c_transform.pos.x

    if c_player_state.facing == FacingDirection.RIGHT:
        target = player_x - c_viewport.screen_width / 4
    else:
        target = player_x - 3 * c_viewport.screen_width / 4

    diff = target - c_viewport.origin_x
    if c_viewport.world_width > 0:
        half = c_viewport.world_width / 2
        if diff < -half:
            diff += c_viewport.world_width
        elif diff > half:
            diff -= c_viewport.world_width

    lines = [
        f"cam:{c_viewport.origin_x:.0f}",
        f"diff:{diff:.1f}",
        f"trans:{c_viewport.in_transition}",
        f"delay:{c_viewport.transition_timer:.2f}",
    ]

    screen_w = screen.get_width()
    card_x = screen_w - max(len(l) for l in lines) * 6 - _PADDING * 2 - 2
    card_y = _PADDING

    _draw_info_card(screen, lines, card_x, card_y, _COLOR)


def _draw_info_card(screen: pygame.Surface, lines: list[str],
                    x: int, y: int, color: pygame.Color):
    if not lines:
        return

    panel_width = max(len(line) for line in lines) * 6 + _PADDING * 2
    panel_height = len(lines) * _LINE_HEIGHT + _PADDING * 2

    x = max(0, min(x, screen.get_width() - panel_width))
    y = max(0, min(y, screen.get_height() - panel_height))

    panel_surface = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
    panel_surface.fill(_BG_COLOR)
    screen.blit(panel_surface, (x, y))

    for i, line in enumerate(lines):
        text_surface = _font.render(line, False, color)
        screen.blit(text_surface, (x + _PADDING,
                                   y + _PADDING + i * _LINE_HEIGHT))
