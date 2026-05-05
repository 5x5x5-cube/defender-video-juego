import random

import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_star_blink import CStarBlink
from src.ecs.load.load_world import BlinkRateConfig


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
