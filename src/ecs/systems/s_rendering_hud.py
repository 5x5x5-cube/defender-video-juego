import pygame

from src.ecs.load.load_world import InterfaceConfig
from src.engine.service_locator import ServiceLocator


def system_rendering_hud(screen: pygame.Surface, interface_cfg: InterfaceConfig):
    hud_height = interface_cfg["hud_height"]
    screen_width = screen.get_width()
    hud_line_color = interface_cfg["hud_line_color"]

    _draw_hud_separator(screen, screen_width, hud_height, hud_line_color)
    _draw_score(screen, interface_cfg)
    _draw_lives(screen, interface_cfg)
    _draw_smart_bombs(screen, interface_cfg)
    _draw_radar_placeholder(screen, interface_cfg)


def _draw_hud_separator(screen: pygame.Surface, screen_width: int,
                        hud_height: int, color: pygame.Color):
    pygame.draw.line(screen, color, (0, hud_height), (screen_width, hud_height))


def _draw_lives(screen: pygame.Surface, interface_cfg: InterfaceConfig):
    lives_img = ServiceLocator.images_service.get("assets/img/interface_lives.png")
    for i in range(3):
        screen.blit(lives_img, (4 + i * (lives_img.get_width() + 2), 2))


def _draw_score(screen: pygame.Surface, interface_cfg: InterfaceConfig):
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)
    score_text = font.render("00000", False, interface_cfg["normal_text_color"])
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
