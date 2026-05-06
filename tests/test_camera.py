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
LERP_SPEED = 100
NO_DELAY = 0


def _create_world_with_camera(player_x=0, facing=FacingDirection.RIGHT):
    world = esper.World()
    player = world.create_entity()
    c_state = CPlayerState()
    c_state.facing = facing
    world.add_component(player, CTransform(pygame.Vector2(player_x, 128)))
    world.add_component(player, CVelocity(pygame.Vector2(0, 0)))
    world.add_component(player, c_state)
    world.add_component(player, CTagPlayer())

    viewport = world.create_entity()
    c_viewport = CViewport(WORLD_WIDTH, SCREEN_WIDTH)
    c_viewport.last_facing = facing
    world.add_component(viewport, c_viewport)
    return world


class TestCameraFollowsPlayer:
    def test_viewport_moves_toward_player_facing_right(self):
        world = _create_world_with_camera(player_x=500, facing=FacingDirection.RIGHT)

        for _ in range(60):
            system_camera(world, 1.0 / 60, LERP_SPEED, LERP_SPEED, NO_DELAY)

        viewport = world.get_component(CViewport)[0][1]
        assert viewport.origin_x == pytest.approx(500 - SCREEN_WIDTH / 4, abs=5)

    def test_viewport_moves_toward_player_facing_left(self):
        world = _create_world_with_camera(player_x=500, facing=FacingDirection.LEFT)

        for _ in range(60):
            system_camera(world, 1.0 / 60, LERP_SPEED, LERP_SPEED, NO_DELAY)

        viewport = world.get_component(CViewport)[0][1]
        assert viewport.origin_x == pytest.approx(500 - 3 * SCREEN_WIDTH / 4, abs=5)


class TestCameraLerp:
    def test_viewport_does_not_snap_instantly(self):
        world = _create_world_with_camera(player_x=500, facing=FacingDirection.RIGHT)

        system_camera(world, 1.0 / 60, 2.5, 2.5, NO_DELAY)

        viewport = world.get_component(CViewport)[0][1]
        target = 500 - SCREEN_WIDTH / 4
        assert 0 < viewport.origin_x < target

    def test_lerp_converges_to_target(self):
        world = _create_world_with_camera(player_x=500, facing=FacingDirection.RIGHT)
        target = 500 - SCREEN_WIDTH / 4

        for _ in range(300):
            system_camera(world, 1.0 / 60, 5.0, 5.0, NO_DELAY)

        viewport = world.get_component(CViewport)[0][1]
        assert viewport.origin_x == pytest.approx(target, abs=1)


class TestCameraWorldWrap:
    def test_camera_takes_shortest_path_across_boundary(self):
        world = _create_world_with_camera(player_x=50, facing=FacingDirection.RIGHT)
        viewport = world.get_component(CViewport)[0][1]
        viewport.origin_x = 3100

        system_camera(world, 1.0 / 60, LERP_SPEED, LERP_SPEED, NO_DELAY)

        assert viewport.origin_x > 3100 or viewport.origin_x < 50

    def test_camera_origin_stays_within_world_bounds(self):
        world = _create_world_with_camera(player_x=500, facing=FacingDirection.RIGHT)

        for _ in range(60):
            system_camera(world, 1.0 / 60, LERP_SPEED, LERP_SPEED, NO_DELAY)

        viewport = world.get_component(CViewport)[0][1]
        assert 0 <= viewport.origin_x < WORLD_WIDTH


class TestCameraTransitionDelay:
    def test_camera_freezes_during_delay(self):
        world = _create_world_with_camera(player_x=500, facing=FacingDirection.RIGHT)
        viewport = world.get_component(CViewport)[0][1]
        viewport.origin_x = 420

        player_state = world.get_component(CPlayerState)[0][1]
        player_state.facing = FacingDirection.LEFT

        system_camera(world, 1.0 / 60, LERP_SPEED, LERP_SPEED, 0.5)

        assert viewport.origin_x == 420

    def test_camera_moves_after_delay_expires(self):
        world = _create_world_with_camera(player_x=500, facing=FacingDirection.RIGHT)
        viewport = world.get_component(CViewport)[0][1]
        viewport.origin_x = 420

        player_state = world.get_component(CPlayerState)[0][1]
        player_state.facing = FacingDirection.LEFT

        for _ in range(30):
            system_camera(world, 1.0 / 60, LERP_SPEED, LERP_SPEED, 0.1)

        assert viewport.origin_x != 420
