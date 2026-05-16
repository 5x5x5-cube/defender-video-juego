import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_mutant import CTagMutant
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.load.load_world import MutantConfig


def system_enemy_mutant_state(world: esper.World, mutant_cfg: MutantConfig):
    player_pos = _get_player_pos(world)
    if player_pos is None:
        return

    speed = mutant_cfg["speed"]

    for _, (c_transform, c_velocity, _) in world.get_components(
            CTransform, CVelocity, CTagMutant):
        direction = player_pos - c_transform.pos
        if direction.length() > 0:
            c_velocity.vel = direction.normalize() * speed


def _get_player_pos(world: esper.World):
    for _, (c_transform, _) in world.get_components(CTransform, CTagPlayer):
        return c_transform.pos.copy()
    return None
