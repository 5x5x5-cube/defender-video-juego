import random

import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_parallax import CParallax
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_star_blink import CStarBlink
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_player_burner import CTagPlayerBurner
from src.ecs.load.load_world import BlinkRateConfig, BulletConfig, PlayerConfig
from src.ecs.components.c_player_state import FacingDirection
from src.engine.service_locator import ServiceLocator


def create_star(world: esper.World,
                world_width: float,
                screen_height: int,
                star_colors: list[pygame.Color],
                blink_rate_cfg: BlinkRateConfig,
                parallax_factor: float) -> int:
    color = random.choice(star_colors)
    parallax_width = world_width * parallax_factor
    pos = pygame.Vector2(
        random.uniform(0, parallax_width),
        random.randint(0, screen_height - 1)
    )
    rate = random.uniform(blink_rate_cfg["min"], blink_rate_cfg["max"])

    star_entity = world.create_entity()
    world.add_component(star_entity, CTransform(pos))
    world.add_component(star_entity, CSurface(pygame.Vector2(1, 1), color))
    world.add_component(star_entity, CStarBlink(rate, color))
    world.add_component(star_entity, CParallax(parallax_factor))
    return star_entity


def create_player(world: esper.World, player_cfg: PlayerConfig) -> int:
    player_surface = ServiceLocator.images_service.get(player_cfg["image"])
    player_entity = world.create_entity()
    world.add_component(player_entity, CTransform(player_cfg["initial_position"].copy()))
    world.add_component(player_entity, CVelocity(pygame.Vector2(0, 0)))
    world.add_component(player_entity, CSurface.from_surface(player_surface))
    world.add_component(player_entity, CPlayerState())
    world.add_component(player_entity, CTagPlayer())
    return player_entity


def create_player_burner(world: esper.World, player_cfg: PlayerConfig,
                         player_pos: pygame.Vector2) -> int:
    burner_anim = player_cfg["animations"]["burner"]["idle"]
    burner_surface = ServiceLocator.images_service.get(burner_anim["image"])
    burner_entity = world.create_entity()
    frame_width = burner_surface.get_width() // burner_anim["number_frames"]
    burner_pos = pygame.Vector2(
        player_pos.x - frame_width,
        player_pos.y
    )
    world.add_component(burner_entity, CTransform(burner_pos))
    c_surface = CSurface.from_surface(burner_surface)
    frame_width = burner_surface.get_width() // burner_anim["number_frames"]
    c_surface.area = pygame.Rect(0, 0, frame_width, burner_surface.get_height())
    world.add_component(burner_entity, c_surface)
    world.add_component(burner_entity, CAnimation(
        burner_anim["number_frames"], burner_anim["list"]))
    world.add_component(burner_entity, CTagPlayerBurner())
    return burner_entity


def create_viewport(world: esper.World, world_width: float,
                    screen_width: float) -> int:
    viewport_entity = world.create_entity()
    world.add_component(viewport_entity, CViewport(world_width, screen_width))
    return viewport_entity


def create_terrain(world: esper.World, world_width: float,
                   screen_height: int, num_points: int,
                   color: pygame.Color, parallax_factor: float) -> int:
    terrain_width = int(world_width * parallax_factor)
    terrain_height = screen_height
    points = _generate_terrain_points(terrain_width, terrain_height, num_points)

    surface = pygame.Surface((terrain_width, terrain_height), pygame.SRCALPHA)
    pygame.draw.lines(surface, color, False, points)

    terrain_entity = world.create_entity()
    world.add_component(terrain_entity, CTransform(pygame.Vector2(0, 0)))
    world.add_component(terrain_entity, CSurface.from_surface(surface))
    world.add_component(terrain_entity, CParallax(parallax_factor))
    return terrain_entity


def _generate_terrain_points(width: int, height: int,
                             num_points: int) -> list[tuple[int, int]]:
    min_y = int(height * 0.75)
    max_y = height - 5
    max_step = max(1, (max_y - min_y) // 8)
    spacing = width / (num_points - 1) if num_points > 1 else width

    first_y = random.randint(min_y, max_y)
    y = first_y
    return_start = int(num_points * 0.85)
    points = []
    for i in range(num_points - 1):
        x = int(i * spacing)
        points.append((x, y))
        step = _terrain_step(y, first_y, max_step, i, return_start, num_points, max_y)
        y = max(min_y, min(max_y, y + step))
    points.append((width, first_y))

    return points


def _terrain_step(y: int, target_y: int, max_step: int,
                  index: int, return_start: int, num_points: int,
                  max_y: int) -> int:
    floor_bias = 1 if y < max_y else -1
    step = random.randint(-max_step, max_step) + floor_bias

    if index >= return_start:
        bias_strength = (index - return_start) / (num_points - 1 - return_start)
        direction = 1 if target_y > y else -1
        return_bias = int(max_step * bias_strength * direction)
        step += return_bias

    return max(-max_step * 2, min(max_step * 2, step))


def create_bullet(world: esper.World, player_pos: pygame.Vector2,
                  player_width: int, player_height: int,
                  facing: FacingDirection, bullet_cfg: BulletConfig) -> int:
    bullet_w = bullet_cfg["width"]
    bullet_h = bullet_cfg["height"]
    speed = bullet_cfg["speed"] * facing.value

    if facing == FacingDirection.RIGHT:
        bullet_x = player_pos.x + player_width
    else:
        bullet_x = player_pos.x - bullet_w

    bullet_y = player_pos.y + player_height // 2 - bullet_h // 2

    bullet_entity = world.create_entity()
    world.add_component(bullet_entity, CTransform(pygame.Vector2(bullet_x, bullet_y)))
    world.add_component(bullet_entity, CVelocity(pygame.Vector2(speed, 0)))
    world.add_component(bullet_entity,
                        CSurface(pygame.Vector2(bullet_w, bullet_h),
                                 pygame.Color(255, 255, 255)))
    world.add_component(bullet_entity, CTagBullet())
    return bullet_entity


def create_input_commands(world: esper.World):
    world.create_entity(CInputCommand("MOVE_RIGHT", pygame.K_RIGHT))
    world.create_entity(CInputCommand("MOVE_LEFT", pygame.K_LEFT))
    world.create_entity(CInputCommand("MOVE_UP", pygame.K_UP))
    world.create_entity(CInputCommand("MOVE_DOWN", pygame.K_DOWN))
    world.create_entity(CInputCommand("FIRE", pygame.K_s))
