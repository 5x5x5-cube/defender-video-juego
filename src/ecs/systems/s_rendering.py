import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface


def system_rendering(world: esper.World, screen: pygame.Surface):
    for _, (c_transform, c_surface) in world.get_components(CTransform, CSurface):
        screen.blit(c_surface.surf, (c_transform.pos.x, c_transform.pos.y), c_surface.area)
