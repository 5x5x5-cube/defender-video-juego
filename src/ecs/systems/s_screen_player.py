import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_screen_player(world: esper.World, screen_rect: pygame.Rect):
    for _, (c_transform, c_surface, _) in world.get_components(
            CTransform, CSurface, CTagPlayer):
        sprite_rect = c_surface.get_area_relative(c_transform.pos)

        if sprite_rect.left < 0:
            c_transform.pos.x = 0
        elif sprite_rect.right > screen_rect.width:
            c_transform.pos.x = screen_rect.width - sprite_rect.width

        if sprite_rect.top < 0:
            c_transform.pos.y = 0
        elif sprite_rect.bottom > screen_rect.height:
            c_transform.pos.y = screen_rect.height - sprite_rect.height
