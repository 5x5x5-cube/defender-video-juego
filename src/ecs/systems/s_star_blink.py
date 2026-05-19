import esper
import pygame

from src.ecs.components.c_star_blink import CStarBlink
from src.ecs.components.c_surface import CSurface


def system_star_blink(world: esper.World, delta_time: float):
    for _, (c_star_blink, c_surface) in world.get_components(CStarBlink, CSurface):
        c_star_blink.timer += delta_time
        if c_star_blink.timer >= c_star_blink.rate:
            c_star_blink.timer = 0.0
            c_star_blink.visible = not c_star_blink.visible
            _toggle_star_visibility(c_star_blink, c_surface)


def _toggle_star_visibility(c_star_blink: CStarBlink, c_surface: CSurface):
    if c_star_blink.visible:
        c_surface.surf.fill(c_star_blink.color)
    else:
        c_surface.surf.fill(pygame.Color(0, 0, 0, 0))
