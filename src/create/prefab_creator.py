import random

import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_parallax import CParallax
from src.ecs.components.c_terrain import CTerrain
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_star_blink import CStarBlink
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.c_enemy_lander_state import CEnemyLanderState
from src.ecs.components.c_particle_lifetime import CParticleLifetime
from src.ecs.components.c_humanoid_state import CHumanoidState
from src.ecs.components.c_shoot_timer import CShootTimer
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_humanoid import CTagHumanoid
from src.ecs.components.tags.c_tag_player_burner import CTagPlayerBurner
from src.ecs.load.load_world import BlinkRateConfig, BulletConfig, LanderConfig, PlayerConfig
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
                   color: pygame.Color, bg_color: pygame.Color,
                   parallax_factor: float) -> int:
    terrain_width = int(world_width * parallax_factor)
    terrain_height = screen_height
    points = _generate_terrain_points(terrain_width, terrain_height, num_points)

    surface = pygame.Surface((terrain_width, terrain_height), pygame.SRCALPHA)
    fill_points = points + [(terrain_width, terrain_height), (0, terrain_height)]
    pygame.draw.polygon(surface, bg_color, fill_points)
    pygame.draw.lines(surface, color, False, points)

    terrain_entity = world.create_entity()
    world.add_component(terrain_entity, CTransform(pygame.Vector2(0, 0)))
    world.add_component(terrain_entity, CSurface.from_surface(surface))
    world.add_component(terrain_entity, CParallax(parallax_factor))
    world.add_component(terrain_entity, CTerrain(points))
    return terrain_entity


def _generate_terrain_points(width: int, height: int,
                             num_points: int) -> list[tuple[int, int]]:
    min_y = int(height * 0.65)
    max_y = height - 30
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

    bullet_y = round(player_pos.y) + player_height // 2 - bullet_h // 2
    surface = _create_laser_surface(bullet_w, bullet_h, facing)

    bullet_entity = world.create_entity()
    world.add_component(bullet_entity, CTransform(pygame.Vector2(bullet_x, bullet_y)))
    world.add_component(bullet_entity, CVelocity(pygame.Vector2(speed, 0)))
    world.add_component(bullet_entity, CSurface.from_surface(surface))
    world.add_component(bullet_entity, CTagBullet())
    return bullet_entity


def _create_laser_surface(width: int, height: int,
                          facing: FacingDirection) -> pygame.Surface:
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    tip_color = pygame.Color(255, 255, 255)
    trail_color = pygame.Color(0, 255, 0)

    for x in range(width):
        if facing == FacingDirection.RIGHT:
            t = x / max(1, width - 1)
        else:
            t = 1 - x / max(1, width - 1)
        r = int(trail_color.r + (tip_color.r - trail_color.r) * t)
        g = int(trail_color.g + (tip_color.g - trail_color.g) * t)
        b = int(trail_color.b + (tip_color.b - trail_color.b) * t)
        for y in range(height):
            surface.set_at((x, y), pygame.Color(r, g, b))

    return surface


def create_humanoid(world: esper.World, world_x: float,
                    screen_height: int, c_terrain: CTerrain) -> int:
    humanoid_surface = ServiceLocator.images_service.get("assets/img/astronaut.png")
    num_frames = 3
    frame_width = humanoid_surface.get_width() // num_frames
    humanoid_height = humanoid_surface.get_height()
    terrain_y = c_terrain.surface_height_at(world_x)
    min_y = terrain_y
    max_y = screen_height - humanoid_height
    pos_y = random.uniform(min_y, max_y) if max_y > min_y else min_y

    humanoid_entity = world.create_entity()
    world.add_component(humanoid_entity, CTransform(pygame.Vector2(world_x, pos_y)))
    world.add_component(humanoid_entity, CVelocity(pygame.Vector2(0, 0)))
    c_surface = CSurface.from_surface(humanoid_surface)
    c_surface.area = pygame.Rect(0, 0, frame_width, humanoid_height)
    world.add_component(humanoid_entity, c_surface)
    world.add_component(humanoid_entity, CAnimation(num_frames,
        [{"name": "walk", "start": 0, "end": 2, "framerate": 4}]))
    world.add_component(humanoid_entity, CHumanoidState(world_x))
    world.add_component(humanoid_entity, CTagHumanoid())
    return humanoid_entity


def create_humanoids(world: esper.World, world_width: float,
                     screen_height: int, count: int):
    c_terrain = None
    for _, terrain in world.get_component(CTerrain):
        c_terrain = terrain
        break
    if c_terrain is None:
        return

    for _ in range(count):
        world_x = random.uniform(0, world_width)
        create_humanoid(world, world_x, screen_height, c_terrain)


def create_enemy_lander(world: esper.World, world_x: float,
                        lander_cfg: LanderConfig) -> int:
    lander_surface = ServiceLocator.images_service.get(lander_cfg["image"])
    anim_cfg = lander_cfg["animations"]
    num_frames = anim_cfg["number_frames"]
    frame_width = lander_surface.get_width() // num_frames
    lander_height = lander_surface.get_height()

    lander_entity = world.create_entity()
    world.add_component(lander_entity, CTransform(pygame.Vector2(world_x, -lander_height)))
    world.add_component(lander_entity, CVelocity(pygame.Vector2(0, 0)))
    c_surface = CSurface.from_surface(lander_surface)
    c_surface.area = pygame.Rect(0, 0, frame_width, lander_height)
    world.add_component(lander_entity, c_surface)
    world.add_component(lander_entity, CAnimation(num_frames, anim_cfg["list"]))
    world.add_component(lander_entity, CEnemyLanderState())
    world.add_component(lander_entity, CShootTimer(
        lander_cfg["shoot_cooldown_min"], lander_cfg["shoot_cooldown_max"]))
    world.add_component(lander_entity, CTagEnemy())
    return lander_entity


def create_enemy_bullet(world: esper.World, origin_pos: pygame.Vector2,
                        target_pos: pygame.Vector2, lander_cfg: LanderConfig) -> int:
    direction = target_pos - origin_pos
    if direction.length() > 0:
        direction = direction.normalize()
    else:
        direction = pygame.Vector2(1, 0)

    speed = lander_cfg["bullet_speed"]
    bullet_surface = ServiceLocator.images_service.get(lander_cfg["bullet_image"])

    bullet_entity = world.create_entity()
    world.add_component(bullet_entity, CTransform(origin_pos.copy()))
    world.add_component(bullet_entity, CVelocity(direction * speed))
    world.add_component(bullet_entity, CSurface.from_surface(bullet_surface))
    world.add_component(bullet_entity, CTagEnemyBullet())
    return bullet_entity


def _spawn_particles(world: esper.World, pos: pygame.Vector2,
                     num_particles: int, speed: float, lifetime: float,
                     colors: list[pygame.Color], sizes: list[int]):
    for _ in range(num_particles):
        angle = random.uniform(0, 360)
        particle_speed = random.uniform(speed * 0.3, speed)
        vel = pygame.Vector2(particle_speed, 0).rotate(angle)
        particle_lifetime = random.uniform(lifetime * 0.3, lifetime)
        color = random.choice(colors)
        size = random.choice(sizes)

        particle = world.create_entity()
        world.add_component(particle, CTransform(pos.copy()))
        world.add_component(particle, CVelocity(vel))
        world.add_component(particle, CSurface(
            pygame.Vector2(size, size), color))
        world.add_component(particle, CParticleLifetime(particle_lifetime))


def create_ship_explosion(world: esper.World, pos: pygame.Vector2):
    colors = [
        pygame.Color(255, 255, 255),
        pygame.Color(255, 255, 200),
        pygame.Color(255, 200, 100),
        pygame.Color(200, 150, 50),
    ]
    _spawn_particles(world, pos, num_particles=50, speed=100,
                     lifetime=1.0, colors=colors, sizes=[1, 2, 2, 3])


def create_enemy_explosion(world: esper.World, pos: pygame.Vector2):
    colors = [pygame.Color(0, 255, 0)]
    _spawn_particles(world, pos, num_particles=15, speed=60,
                     lifetime=0.5, colors=colors, sizes=[1, 2])


def create_humanoid_explosion(world: esper.World, pos: pygame.Vector2):
    colors = [pygame.Color(255, 100, 255)]
    _spawn_particles(world, pos, num_particles=10, speed=40,
                     lifetime=0.4, colors=colors, sizes=[1, 1, 2])


def create_input_commands(world: esper.World):
    world.create_entity(CInputCommand("MOVE_RIGHT", pygame.K_RIGHT))
    world.create_entity(CInputCommand("MOVE_LEFT", pygame.K_LEFT))
    world.create_entity(CInputCommand("MOVE_UP", pygame.K_UP))
    world.create_entity(CInputCommand("MOVE_DOWN", pygame.K_DOWN))
    world.create_entity(CInputCommand("FIRE", pygame.K_s))
