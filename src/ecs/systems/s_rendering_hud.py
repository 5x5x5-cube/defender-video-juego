import esper
import pygame

from src.ecs.components.c_enemy_lander_state import CEnemyLanderState, LanderState
from src.ecs.components.c_humanoid_state import CHumanoidState
from src.ecs.components.c_terrain import CTerrain
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_humanoid import CTagHumanoid
from src.ecs.components.tags.c_tag_mutant import CTagMutant
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.load.load_world import InterfaceConfig
from src.engine.service_locator import ServiceLocator
import src.engine.game_state as game_state


def system_rendering_hud(screen: pygame.Surface, interface_cfg: InterfaceConfig,
                         world: esper.World, game_height: int = 220,
                         world_width: float = 3200):
    hud_height = interface_cfg["hud_height"]
    screen_width = screen.get_width()
    hud_line_color = interface_cfg["hud_line_color"]

    _draw_hud_separator(screen, screen_width, hud_height, hud_line_color)
    _draw_score(screen, interface_cfg)
    _draw_lives(screen, interface_cfg)
    _draw_smart_bombs(screen, interface_cfg)
    _draw_radar(screen, interface_cfg, world, game_height, world_width)
    _draw_enemy_counter(screen, interface_cfg, world)
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
    for i in range(game_state.smart_bombs):
        screen.blit(bomb_img, (bomb_x, 4 + i * (bomb_img.get_height() + 1)))


def _draw_radar(screen: pygame.Surface, interface_cfg: InterfaceConfig,
                world: esper.World, game_height: int, world_width: float):
    radar_w = interface_cfg["radar_width"]
    radar_h = interface_cfg["radar_height"]
    hud_height = interface_cfg["hud_height"]
    screen_width = screen.get_width()

    radar_left = (screen_width - radar_w) // 2
    radar_top = (hud_height - radar_h) // 2

    radar_surf = pygame.Surface((radar_w, radar_h))
    radar_surf.fill(pygame.Color(0, 0, 20))

    scale_x = radar_w / world_width
    scale_y = radar_h / game_height

    # Terrain line
    c_terrain = _get_terrain(world)
    if c_terrain and len(c_terrain.points) > 1:
        step = max(1, len(c_terrain.points) // radar_w)
        pts = [(int(px * scale_x), int(py * scale_y))
               for px, py in c_terrain.points[::step]]
        if len(pts) > 1:
            pygame.draw.lines(radar_surf, pygame.Color(120, 50, 50), False, pts, 1)

    # Viewport highlight
    c_viewport = _get_viewport(world)
    if c_viewport is not None:
        vp_left = int((c_viewport.origin_x / world_width) * radar_w) % radar_w
        vp_w = max(1, int((c_viewport.screen_width / world_width) * radar_w))
        pygame.draw.rect(radar_surf, pygame.Color(30, 30, 80),
                         (vp_left, 0, vp_w, radar_h))

    # Humanoids — pink dots
    for _, (c_transform, _, _) in world.get_components(CTransform, CHumanoidState, CTagHumanoid):
        hx = int((c_transform.pos.x / world_width) * radar_w) % radar_w
        hy = max(0, min(radar_h - 1, int((c_transform.pos.y / game_height) * radar_h)))
        pygame.draw.rect(radar_surf, pygame.Color(255, 150, 255), (hx, hy, 1, 1))

    # Enemies — green (lander), yellow (capturing), orange (mutant)
    for entity, (c_transform, _) in world.get_components(CTransform, CTagEnemy):
        if world.has_component(entity, CTagMutant):
            color = pygame.Color(255, 120, 0)
        elif world.has_component(entity, CEnemyLanderState):
            ls = world.component_for_entity(entity, CEnemyLanderState)
            color = (pygame.Color(255, 255, 0)
                     if ls.state == LanderState.CAPTURE
                     else pygame.Color(0, 220, 0))
        else:
            color = pygame.Color(0, 220, 0)
        ex = int((c_transform.pos.x / world_width) * radar_w) % radar_w
        ey = max(0, min(radar_h - 2, int((c_transform.pos.y / game_height) * radar_h)))
        pygame.draw.rect(radar_surf, color, (max(0, ex - 1), ey, 2, 2))

    # Player — white dot
    for _, (c_transform, _) in world.get_components(CTransform, CTagPlayer):
        px = int((c_transform.pos.x / world_width) * radar_w) % radar_w
        py = max(0, min(radar_h - 2, int((c_transform.pos.y / game_height) * radar_h)))
        pygame.draw.rect(radar_surf, pygame.Color(255, 255, 255),
                         (max(0, px - 1), py, 3, 2))

    # Border
    pygame.draw.rect(radar_surf, interface_cfg["hud_line_color"],
                     (0, 0, radar_w, radar_h), 1)

    screen.blit(radar_surf, (radar_left, radar_top))


def _draw_enemy_counter(screen: pygame.Surface, interface_cfg: InterfaceConfig,
                        world: esper.World):
    enemy_count = len(world.get_component(CTagEnemy))
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 6)
    label = font.render(f"E:{enemy_count:02d}", False, interface_cfg["normal_text_color"])
    radar_x = (screen.get_width() - interface_cfg["radar_width"]) // 2
    screen.blit(label, (radar_x + interface_cfg["radar_width"] + 4, 4))


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


def _get_terrain(world: esper.World):
    for _, c_terrain in world.get_component(CTerrain):
        return c_terrain
    return None
