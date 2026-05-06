import esper

from src.ecs.components.c_player_state import CPlayerState, FacingDirection
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_player import CTagPlayer


def system_camera(world: esper.World, delta_time: float,
                  lerp_speed: float, transition_lerp_speed: float,
                  transition_delay: float):
    player_data = _get_player_data(world)
    if player_data is None:
        return

    player_x, player_facing, player_speed = player_data

    for _, c_viewport in world.get_component(CViewport):
        _handle_direction_change(c_viewport, player_facing, transition_delay)
        _update_transition_timer(c_viewport, delta_time)

        if _is_waiting(c_viewport):
            continue

        target_x = _calculate_target(player_x, player_facing, c_viewport.screen_width)
        diff = _shortest_circular_distance(c_viewport.origin_x, target_x, c_viewport.world_width)

        if c_viewport.in_transition:
            active_lerp = _transition_lerp(transition_lerp_speed, diff, player_speed)
            if abs(diff) < 1.0:
                c_viewport.in_transition = False
        else:
            active_lerp = lerp_speed

        c_viewport.origin_x = _lerp_toward_target(
            c_viewport.origin_x, diff, active_lerp, delta_time)
        if c_viewport.world_width > 0:
            c_viewport.origin_x = c_viewport.origin_x % c_viewport.world_width


def _get_player_data(world: esper.World):
    for _, (c_transform, c_player_state, c_velocity, _) in world.get_components(
            CTransform, CPlayerState, CVelocity, CTagPlayer):
        return c_transform.pos.x, c_player_state.facing, abs(c_velocity.vel.x)
    return None


def _handle_direction_change(c_viewport: CViewport, player_facing: FacingDirection,
                             transition_delay: float):
    if player_facing != c_viewport.last_facing:
        c_viewport.last_facing = player_facing
        c_viewport.transition_timer = transition_delay
        c_viewport.in_transition = True


def _update_transition_timer(c_viewport: CViewport, delta_time: float):
    if c_viewport.transition_timer > 0:
        c_viewport.transition_timer -= delta_time


def _is_waiting(c_viewport: CViewport) -> bool:
    return c_viewport.transition_timer > 0


def _calculate_target(player_x: float, facing: FacingDirection,
                      screen_width: float) -> float:
    if facing == FacingDirection.RIGHT:
        return player_x - screen_width / 4
    return player_x - 3 * screen_width / 4


def _shortest_circular_distance(current: float, target: float, world_width: float) -> float:
    diff = target - current
    if world_width > 0:
        half_world = world_width / 2
        if diff < -half_world:
            diff += world_width
        elif diff > half_world:
            diff -= world_width
    return diff


def _transition_lerp(base_lerp: float, diff: float, player_speed: float) -> float:
    if abs(diff) < 1 or player_speed < 1:
        return base_lerp
    min_lerp_to_track = player_speed / abs(diff)
    return max(base_lerp, min_lerp_to_track)


def _lerp_toward_target(current: float, diff: float,
                        lerp_speed: float, delta_time: float) -> float:
    if abs(diff) < 0.5:
        return current + diff
    step = diff * lerp_speed * delta_time
    return current + step
