import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface


def system_animation(world: esper.World, delta_time: float):
    for _, (c_surface, c_animation) in world.get_components(CSurface, CAnimation):
        c_animation.current_animation_time -= delta_time
        if c_animation.current_animation_time <= 0:
            current_anim = c_animation.animations[c_animation.current_animation]
            c_animation.current_animation_time = current_anim.framerate
            c_animation.current_frame += 1
            if c_animation.current_frame > current_anim.end:
                c_animation.current_frame = current_anim.start

            frame_width = c_surface.surf.get_width() // c_animation.number_frames
            c_surface.area.width = frame_width
            c_surface.area.x = c_animation.current_frame * frame_width
