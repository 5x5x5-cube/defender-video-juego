import random

import esper

from src.ecs.components.c_enemy_lander_state import CEnemyLanderState, LanderState
from src.ecs.components.c_humanoid_state import CHumanoidState, HumanoidState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_humanoid import CTagHumanoid
from src.ecs.load.load_world import HumanoidConfig
from src.engine.service_locator import ServiceLocator

FALL_SPEED = 50.0


def system_humanoid_state(world: esper.World, humanoid_cfg: HumanoidConfig):
    captors = _get_active_captors(world)

    for humanoid_entity, (c_transform, c_velocity, c_humanoid_state, _) in world.get_components(
            CTransform, CVelocity, CHumanoidState, CTagHumanoid):
        if c_humanoid_state.state == HumanoidState.ON_GROUND:
            _do_on_ground(c_transform, c_velocity, c_humanoid_state, humanoid_cfg)
        elif c_humanoid_state.state == HumanoidState.CAPTURED:
            _do_captured(humanoid_entity, c_humanoid_state, captors)
        elif c_humanoid_state.state == HumanoidState.FALLING:
            _do_falling(c_transform, c_velocity, c_humanoid_state)


def _get_active_captors(world: esper.World) -> set[int]:
    captors = set()
    for _, c_lander_state in world.get_component(CEnemyLanderState):
        if c_lander_state.state == LanderState.CAPTURE and c_lander_state.target_humanoid != -1:
            captors.add(c_lander_state.target_humanoid)
    return captors


def _do_on_ground(c_transform: CTransform, c_velocity: CVelocity,
                  c_humanoid_state: CHumanoidState, humanoid_cfg: HumanoidConfig):
    distance_from_spawn = c_transform.pos.x - c_humanoid_state.spawn_x
    wander_speed = humanoid_cfg["wander_speed"]
    wander_range = humanoid_cfg["wander_range"]

    if abs(distance_from_spawn) >= wander_range:
        c_velocity.vel.x = -wander_speed if distance_from_spawn > 0 else wander_speed
    elif random.random() < humanoid_cfg["direction_change_chance"]:
        c_velocity.vel.x = random.choice([-wander_speed, wander_speed, 0])


def _do_captured(humanoid_entity: int, c_humanoid_state: CHumanoidState,
                 captors: set[int]):
    if humanoid_entity not in captors:
        c_humanoid_state.state = HumanoidState.FALLING


def _do_falling(c_transform: CTransform, c_velocity: CVelocity,
                c_humanoid_state: CHumanoidState):
    if c_velocity.vel.y == 0:
        ServiceLocator.sounds_service.play("assets/snd/astronaut_fall.ogg")

    c_velocity.vel.x = 0
    c_velocity.vel.y = FALL_SPEED

    if c_transform.pos.y >= c_humanoid_state.spawn_y:
        c_transform.pos.y = c_humanoid_state.spawn_y
        c_humanoid_state.spawn_x = c_transform.pos.x
        c_velocity.vel.y = 0
        c_humanoid_state.state = HumanoidState.ON_GROUND
