import random

import esper

from src.ecs.components.c_humanoid_state import CHumanoidState, HumanoidState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_humanoid import CTagHumanoid
from src.ecs.load.load_world import HumanoidConfig


def system_humanoid_state(world: esper.World, humanoid_cfg: HumanoidConfig):
    for _, (c_transform, c_velocity, c_humanoid_state, _) in world.get_components(
            CTransform, CVelocity, CHumanoidState, CTagHumanoid):
        if c_humanoid_state.state == HumanoidState.ON_GROUND:
            _do_on_ground(c_transform, c_velocity, c_humanoid_state, humanoid_cfg)


def _do_on_ground(c_transform: CTransform, c_velocity: CVelocity,
                  c_humanoid_state: CHumanoidState, humanoid_cfg: HumanoidConfig):
    distance_from_spawn = c_transform.pos.x - c_humanoid_state.spawn_x
    wander_speed = humanoid_cfg["wander_speed"]
    wander_range = humanoid_cfg["wander_range"]

    if abs(distance_from_spawn) >= wander_range:
        c_velocity.vel.x = -wander_speed if distance_from_spawn > 0 else wander_speed
    elif random.random() < humanoid_cfg["direction_change_chance"]:
        c_velocity.vel.x = random.choice([-wander_speed, wander_speed, 0])
