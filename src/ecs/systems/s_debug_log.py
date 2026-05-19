import csv
import os
import time

import esper

from src.ecs.components.c_player_state import CPlayerState, FacingDirection
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_player import CTagPlayer

_LOG_FILE = "debug_log.csv"
_writer = None
_file = None
_start_time = None

HEADERS = [
    "time", "player_x", "player_y", "vel_x", "vel_y", "speed",
    "facing", "moving", "cam_origin", "cam_target", "cam_diff",
    "delay_timer", "cam_facing", "ship_screen_x"
]


def system_debug_log(world: esper.World):
    global _writer, _file, _start_time

    if _writer is None:
        _file = open(_LOG_FILE, "w", newline="")
        _writer = csv.writer(_file)
        _writer.writerow(HEADERS)
        _start_time = time.time()

    row = _collect_row(world)
    if row:
        _writer.writerow(row)
        _file.flush()


def close_debug_log():
    global _writer, _file
    if _file:
        _file.close()
        _file = None
        _writer = None


def _collect_row(world: esper.World):
    player_x = player_y = vel_x = vel_y = speed = 0
    facing = "NONE"
    moving = False

    for _, (c_transform, c_velocity, c_player_state, _) in world.get_components(
            CTransform, CVelocity, CPlayerState, CTagPlayer):
        player_x = c_transform.pos.x
        player_y = c_transform.pos.y
        vel_x = c_velocity.vel.x
        vel_y = c_velocity.vel.y
        speed = abs(vel_x)
        facing = c_player_state.facing.name
        moving = c_player_state.moving_horizontal

    for _, c_viewport in world.get_component(CViewport):
        cam_origin = c_viewport.origin_x
        cam_facing = c_viewport.last_facing.name
        delay_timer = c_viewport.transition_timer

        target = _calculate_target(player_x, facing, c_viewport.screen_width)
        diff = _shortest_circular_distance(cam_origin, target, c_viewport.world_width)

        screen_pos = player_x - cam_origin
        if c_viewport.world_width > 0:
            half = c_viewport.world_width / 2
            if screen_pos < -half:
                screen_pos += c_viewport.world_width
            elif screen_pos > half:
                screen_pos -= c_viewport.world_width

        elapsed = time.time() - _start_time

        return [
            f"{elapsed:.3f}", f"{player_x:.1f}", f"{player_y:.1f}",
            f"{vel_x:.1f}", f"{vel_y:.1f}", f"{speed:.1f}",
            facing, moving, f"{cam_origin:.1f}", f"{target:.1f}",
            f"{diff:.1f}", f"{delay_timer:.3f}", cam_facing,
            f"{screen_pos:.1f}"
        ]

    return None


def _calculate_target(player_x: float, facing: str, screen_width: float) -> float:
    if facing == "RIGHT":
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
