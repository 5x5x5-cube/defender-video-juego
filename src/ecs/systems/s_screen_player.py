import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_screen_player(world: esper.World, screen_rect: pygame.Rect,
                         world_width: float = 0):
    for _, (c_transform, c_surface, _) in world.get_components(
            CTransform, CSurface, CTagPlayer):
        sprite_rect = c_surface.get_area_relative(c_transform.pos)

        if world_width > 0:
            c_transform.pos.x = c_transform.pos.x % world_width

        if sprite_rect.top < 0:
            c_transform.pos.y = 0
        elif sprite_rect.bottom > screen_rect.height:
            c_transform.pos.y = screen_rect.height - sprite_rect.height
