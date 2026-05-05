import esper

from src.ecs.components.c_player_state import CPlayerState, FacingDirection
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_camera(world: esper.World, delta_time: float,
                  lerp_speed: float, min_speed: float, max_speed: float):
    player_data = _get_player_data(world)
    if player_data is None:
        return

    player_x, player_facing, player_vel_x = player_data

    for _, c_viewport in world.get_component(CViewport):
        target_x = _calculate_target(player_x, player_facing, c_viewport.screen_width)
        c_viewport.origin_x = _move_toward_target(
            c_viewport.origin_x, target_x, lerp_speed, min_speed,
            player_vel_x, max_speed, delta_time)
        _clamp_to_world_bounds(c_viewport)


def _get_player_data(world: esper.World):
    for _, (c_transform, c_player_state, c_velocity, _) in world.get_components(
            CTransform, CPlayerState, CVelocity, CTagPlayer):
        return c_transform.pos.x, c_player_state.facing, c_velocity.vel.x
    return None


def _calculate_target(player_x: float, facing: FacingDirection,
                      screen_width: float) -> float:
    if facing == FacingDirection.RIGHT:
        return player_x - screen_width / 3
    return player_x - 2 * screen_width / 3


def _move_toward_target(current: float, target: float,
                        lerp_speed: float, min_speed: float,
                        player_vel_x: float, max_speed: float,
                        delta_time: float) -> float:
    diff = target - current
    if _is_close_enough(diff):
        return target

    step = _calculate_lerp_step(diff, lerp_speed, delta_time)
    if _is_moving_with_player(diff, player_vel_x):
        step = _enforce_min_speed(step, diff, min_speed, delta_time,
                                  player_vel_x, max_speed)

    return current + step


def _is_close_enough(diff: float) -> bool:
    return abs(diff) < 0.5


def _calculate_lerp_step(diff: float, lerp_speed: float,
                         delta_time: float) -> float:
    return diff * lerp_speed * delta_time


def _is_moving_with_player(diff: float, player_vel_x: float) -> bool:
    return (diff > 0 and player_vel_x > 0) or (diff < 0 and player_vel_x < 0)


def _enforce_min_speed(step: float, diff: float, min_speed: float,
                       delta_time: float, player_vel_x: float,
                       max_speed: float) -> float:
    speed_ratio = min(abs(player_vel_x) / max_speed, 1.0) if max_speed > 0 else 1.0
    min_step = min_speed * speed_ratio * delta_time
    if abs(step) < min_step:
        return min_step if diff > 0 else -min_step
    return step


def _clamp_to_world_bounds(c_viewport: CViewport):
    if c_viewport.origin_x < 0:
        c_viewport.origin_x = 0
    max_origin = c_viewport.world_width - c_viewport.screen_width
    if c_viewport.origin_x > max_origin:
        c_viewport.origin_x = max_origin
