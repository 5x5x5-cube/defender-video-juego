import random

import esper
import pygame

from src.ecs.components.c_enemy_lander_state import CEnemyLanderState, LanderState
from src.ecs.components.c_humanoid_state import CHumanoidState, HumanoidState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_humanoid import CTagHumanoid
from src.ecs.load.load_world import LanderConfig


def system_enemy_lander_state(world: esper.World, lander_cfg: LanderConfig):
    for lander_entity, (c_transform, c_velocity, c_lander_state, _) in world.get_components(
            CTransform, CVelocity, CEnemyLanderState, CTagEnemy):
        if c_lander_state.state == LanderState.WANDER:
            _do_wander(world, c_transform, c_velocity,
                       c_lander_state, lander_cfg)
        elif c_lander_state.state == LanderState.HUNTING:
            _do_hunting(world, c_transform, c_velocity,
                        c_lander_state, lander_cfg)
        elif c_lander_state.state == LanderState.CAPTURE:
            _do_capture(world, lander_entity, c_transform, c_velocity,
                        c_lander_state, lander_cfg)


def _do_wander(world: esper.World,
               c_transform: CTransform, c_velocity: CVelocity,
               c_lander_state: CEnemyLanderState, lander_cfg: LanderConfig):
    speed = lander_cfg["wander_speed"]

    if random.random() < lander_cfg["direction_change_chance"]:
        c_velocity.vel.x = random.uniform(-speed, speed)
        c_velocity.vel.y = random.uniform(0, speed)

    nearest_humanoid, nearest_distance = _find_nearest_humanoid(world, c_transform.pos)
    if nearest_humanoid is not None and nearest_distance < lander_cfg["bias_range"]:
        c_lander_state.state = LanderState.HUNTING
        c_lander_state.target_humanoid = nearest_humanoid


def _do_hunting(world: esper.World,
                c_transform: CTransform, c_velocity: CVelocity,
                c_lander_state: CEnemyLanderState, lander_cfg: LanderConfig):
    if not world.entity_exists(c_lander_state.target_humanoid):
        c_lander_state.state = LanderState.WANDER
        c_lander_state.target_humanoid = -1
        return

    target_transform = world.component_for_entity(c_lander_state.target_humanoid, CTransform)
    direction = target_transform.pos - c_transform.pos
    distance = direction.length()

    if distance < 5:
        _capture_humanoid(world, c_lander_state)
        return

    speed = lander_cfg["wander_speed"]
    bias_strength = _calculate_bias(distance, lander_cfg)

    random_vel = pygame.Vector2(
        random.uniform(-speed, speed),
        random.uniform(-speed, speed)
    )
    target_vel = direction.normalize() * speed if distance > 0 else pygame.Vector2(0, 0)
    c_velocity.vel = random_vel * (1 - bias_strength) + target_vel * bias_strength


def _do_capture(world: esper.World, lander_entity: int,
                c_transform: CTransform, c_velocity: CVelocity,
                c_lander_state: CEnemyLanderState, lander_cfg: LanderConfig):
    c_velocity.vel.x = 0
    c_velocity.vel.y = -lander_cfg["ascend_speed"]

    if c_lander_state.target_humanoid != -1 and world.entity_exists(c_lander_state.target_humanoid):
        humanoid_transform = world.component_for_entity(
            c_lander_state.target_humanoid, CTransform)
        humanoid_transform.pos.x = c_transform.pos.x
        humanoid_transform.pos.y = c_transform.pos.y + 10

    if c_transform.pos.y < -20:
        if c_lander_state.target_humanoid != -1 and world.entity_exists(c_lander_state.target_humanoid):
            world.delete_entity(c_lander_state.target_humanoid)
        world.delete_entity(lander_entity)


def _capture_humanoid(world: esper.World, c_lander_state: CEnemyLanderState):
    humanoid_state = world.component_for_entity(
        c_lander_state.target_humanoid, CHumanoidState)
    humanoid_state.state = HumanoidState.CAPTURED
    humanoid_velocity = world.component_for_entity(
        c_lander_state.target_humanoid, CVelocity)
    humanoid_velocity.vel.x = 0
    humanoid_velocity.vel.y = 0
    c_lander_state.state = LanderState.CAPTURE


def _find_nearest_humanoid(world: esper.World,
                           lander_pos: pygame.Vector2):
    nearest_entity = None
    nearest_distance = float('inf')

    for humanoid_entity, (c_transform, c_humanoid_state, _) in world.get_components(
            CTransform, CHumanoidState, CTagHumanoid):
        if c_humanoid_state.state != HumanoidState.ON_GROUND:
            continue
        distance = lander_pos.distance_to(c_transform.pos)
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_entity = humanoid_entity

    return nearest_entity, nearest_distance


def _calculate_bias(distance: float, lander_cfg: LanderConfig) -> float:
    bias_range = lander_cfg["bias_range"]
    bias_min = lander_cfg["humanoid_bias_min"]
    bias_max = lander_cfg["humanoid_bias_max"]
    t = 1.0 - min(distance / bias_range, 1.0)
    return bias_min + (bias_max - bias_min) * t
