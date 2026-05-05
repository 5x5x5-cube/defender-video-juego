import esper
import pygame
import pytest

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_player_state import CPlayerState, FacingDirection
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_camera import system_camera


SCREEN_WIDTH = 320
WORLD_WIDTH = 3200
LERP_SPEED = 100  # high speed for tests so lerp converges quickly
MIN_SPEED = 200


def _create_world_with_camera(player_x=0, facing=FacingDirection.RIGHT, vel_x=0):
    world = esper.World()
    player = world.create_entity()
    c_state = CPlayerState()
    c_state.facing = facing
    world.add_component(player, CTransform(pygame.Vector2(player_x, 128)))
    world.add_component(player, CVelocity(pygame.Vector2(vel_x, 0)))
    world.add_component(player, c_state)
    world.add_component(player, CTagPlayer())

    viewport = world.create_entity()
    world.add_component(viewport, CViewport(WORLD_WIDTH, SCREEN_WIDTH))
    return world


class TestCameraFollowsPlayer:
    def test_viewport_moves_toward_player_facing_right(self):
        world = _create_world_with_camera(player_x=500, facing=FacingDirection.RIGHT, vel_x=100)

        for _ in range(60):
            system_camera(world, 1.0 / 60, LERP_SPEED, MIN_SPEED, MIN_SPEED)

        viewport = world.get_component(CViewport)[0][1]
        assert viewport.origin_x == pytest.approx(500 - SCREEN_WIDTH / 3, abs=5)

    def test_viewport_moves_toward_player_facing_left(self):
        world = _create_world_with_camera(player_x=500, facing=FacingDirection.LEFT, vel_x=-100)

        for _ in range(60):
            system_camera(world, 1.0 / 60, LERP_SPEED, MIN_SPEED, MIN_SPEED)

        viewport = world.get_component(CViewport)[0][1]
        assert viewport.origin_x == pytest.approx(500 - 2 * SCREEN_WIDTH / 3, abs=5)


class TestCameraClampsToBounds:
    def test_viewport_does_not_go_below_zero(self):
        world = _create_world_with_camera(player_x=10, facing=FacingDirection.RIGHT)

        for _ in range(60):
            system_camera(world, 1.0 / 60, LERP_SPEED, MIN_SPEED, MIN_SPEED)

        viewport = world.get_component(CViewport)[0][1]
        assert viewport.origin_x == 0

    def test_viewport_does_not_exceed_world_right(self):
        world = _create_world_with_camera(player_x=3190, facing=FacingDirection.RIGHT, vel_x=100)

        for _ in range(60):
            system_camera(world, 1.0 / 60, LERP_SPEED, MIN_SPEED, MIN_SPEED)

        viewport = world.get_component(CViewport)[0][1]
        assert viewport.origin_x == WORLD_WIDTH - SCREEN_WIDTH


class TestCameraLerp:
    def test_viewport_does_not_snap_instantly(self):
        world = _create_world_with_camera(player_x=500, facing=FacingDirection.RIGHT, vel_x=100)

        system_camera(world, 1.0 / 60, 2.5, 50, 200)

        viewport = world.get_component(CViewport)[0][1]
        target = 500 - SCREEN_WIDTH / 3
        assert 0 < viewport.origin_x < target

    def test_min_speed_prevents_camera_falling_behind(self):
        world = _create_world_with_camera(player_x=500, facing=FacingDirection.RIGHT, vel_x=200)
        target = 500 - SCREEN_WIDTH / 3

        # Very low lerp but high min_speed — should still reach target
        for _ in range(120):
            system_camera(world, 1.0 / 60, 0.1, 300, 200)

        viewport = world.get_component(CViewport)[0][1]
        assert viewport.origin_x == pytest.approx(target, abs=5)
