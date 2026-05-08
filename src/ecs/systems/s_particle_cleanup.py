import esper

from src.ecs.components.c_particle_lifetime import CParticleLifetime


def system_particle_cleanup(world: esper.World, delta_time: float):
    for particle_entity, c_lifetime in world.get_component(CParticleLifetime):
        c_lifetime.timer -= delta_time
        if c_lifetime.timer <= 0:
            world.delete_entity(particle_entity)
