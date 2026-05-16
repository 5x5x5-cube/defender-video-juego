import esper
import pygame

from src.ecs.components.c_enemy_lander_state import CEnemyLanderState, LanderState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_viewport import CViewport
from src.ecs.load.load_world import InterfaceConfig
from src.engine.service_locator import ServiceLocator
import src.engine.game_state as game_state


def system_rendering_hud(screen: pygame.Surface, interface_cfg: InterfaceConfig,
                         world: esper.World):
    hud_height = interface_cfg["hud_height"]
    screen_width = screen.get_width()
    hud_line_color = interface_cfg["hud_line_color"]

    _draw_hud_separator(screen, screen_width, hud_height, hud_line_color)
    _draw_score(screen, interface_cfg)
    _draw_lives(screen, interface_cfg)
    _draw_smart_bombs(screen, interface_cfg)
    _draw_radar_placeholder(screen, interface_cfg)
    _draw_capture_arrows(screen, interface_cfg, world)


def _draw_hud_separator(screen: pygame.Surface, screen_width: int,
                        hud_height: int, color: pygame.Color):
    pygame.draw.line(screen, color, (0, hud_height), (screen_width, hud_height))


def _draw_lives(screen: pygame.Surface, interface_cfg: InterfaceConfig):
    lives_img = ServiceLocator.images_service.get("assets/img/interface_lives.png")
    for i in range(game_state.lives):
        screen.blit(lives_img, (4 + i * (lives_img.get_width() + 2), 2))


def _draw_score(screen: pygame.Surface, interface_cfg: InterfaceConfig):
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)
    score_str = str(game_state.score).zfill(5)
    score_text = font.render(score_str, False, interface_cfg["normal_text_color"])
    bomb_img = ServiceLocator.images_service.get("assets/img/interface_smart_bomb.png")
    radar_x = (screen.get_width() - interface_cfg["radar_width"]) // 2
    score_x = radar_x - bomb_img.get_width() - score_text.get_width() - 8
    screen.blit(score_text, (score_x, 14))


def _draw_smart_bombs(screen: pygame.Surface, interface_cfg: InterfaceConfig):
    bomb_img = ServiceLocator.images_service.get("assets/img/interface_smart_bomb.png")
    radar_x = (screen.get_width() - interface_cfg["radar_width"]) // 2
    bomb_x = radar_x - bomb_img.get_width() - 4
    for i in range(3):
        screen.blit(bomb_img, (bomb_x, 4 + i * (bomb_img.get_height() + 1)))


def _draw_radar_placeholder(screen: pygame.Surface, interface_cfg: InterfaceConfig):
    radar_width = interface_cfg["radar_width"]
    hud_height = interface_cfg["hud_height"]
    screen_width = screen.get_width()
    radar_x = (screen_width - radar_width) // 2
    pygame.draw.rect(screen, interface_cfg["hud_line_color"],
                     (radar_x, 0, radar_width, hud_height), 1)


def _draw_capture_arrows(screen: pygame.Surface, interface_cfg: InterfaceConfig,
                         world: esper.World):
    c_viewport = _get_viewport(world)
    if c_viewport is None:
        return

    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 6)
    arrow_color = pygame.Color(255, 200, 0)
    hud_height = interface_cfg["hud_height"]
    screen_width = screen.get_width()

    for _, (c_transform, c_lander_state) in world.get_components(
            CTransform, CEnemyLanderState):
        if c_lander_state.state != LanderState.CAPTURE:
            continue

        screen_x = c_viewport.world_to_screen_x(c_transform.pos.x)

        if screen_x < 0:
            label = font.render("< CAPTURE", False, arrow_color)
            screen.blit(label, (2, hud_height // 2 - label.get_height() // 2))
        elif screen_x > screen_width:
            label = font.render("CAPTURE >", False, arrow_color)
            screen.blit(label, (screen_width - label.get_width() - 2,
                                hud_height // 2 - label.get_height() // 2))


def _get_viewport(world: esper.World):
    for _, c_viewport in world.get_component(CViewport):
        return c_viewport
    return None
