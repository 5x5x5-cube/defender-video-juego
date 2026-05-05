import random

import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_star_blink import CStarBlink
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_burner import CTagPlayerBurner
from src.ecs.load.load_world import BlinkRateConfig, PlayerConfig
from src.engine.service_locator import ServiceLocator


def create_star(world: esper.World,
                screen_rect: pygame.Rect,
                star_colors: list[pygame.Color],
                blink_rate_cfg: BlinkRateConfig) -> int:
    color = random.choice(star_colors)
    pos = pygame.Vector2(
        random.randint(0, screen_rect.width - 1),
        random.randint(0, screen_rect.height - 1)
    )
    rate = random.uniform(blink_rate_cfg["min"], blink_rate_cfg["max"])

    star_entity = world.create_entity()
    world.add_component(star_entity, CTransform(pos))
    world.add_component(star_entity, CSurface(pygame.Vector2(1, 1), color))
    world.add_component(star_entity, CStarBlink(rate, color))
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
    burner_surface = ServiceLocator.images_service.get(player_cfg["burner_idle_image"])
    burner_entity = world.create_entity()
    burner_pos = pygame.Vector2(
        player_pos.x - burner_surface.get_width(),
        player_pos.y
    )
    world.add_component(burner_entity, CTransform(burner_pos))
    world.add_component(burner_entity, CSurface.from_surface(burner_surface))
    world.add_component(burner_entity, CTagPlayerBurner())
    return burner_entity


def create_input_commands(world: esper.World):
    world.create_entity(CInputCommand("MOVE_RIGHT", pygame.K_RIGHT))
    world.create_entity(CInputCommand("MOVE_LEFT", pygame.K_LEFT))
    world.create_entity(CInputCommand("MOVE_UP", pygame.K_UP))
    world.create_entity(CInputCommand("MOVE_DOWN", pygame.K_DOWN))
