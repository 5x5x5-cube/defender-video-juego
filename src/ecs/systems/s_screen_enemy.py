import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_screen_enemy(world: esper.World, screen_rect: pygame.Rect):
    for _, (c_transform, c_surface, _) in world.get_components(
            CTransform, CSurface, CTagEnemy):
        sprite_height = c_surface.area.height

        if c_transform.pos.y < 0:
            c_transform.pos.y = 0
        elif c_transform.pos.y + sprite_height > screen_rect.height:
            c_transform.pos.y = screen_rect.height - sprite_height
