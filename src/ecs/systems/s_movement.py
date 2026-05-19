import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_movement(world: esper.World, delta_time: float):
    for _, (c_transform, c_velocity) in world.get_components(CTransform, CVelocity):
        c_transform.pos.x += c_velocity.vel.x * delta_time
        c_transform.pos.y += c_velocity.vel.y * delta_time
