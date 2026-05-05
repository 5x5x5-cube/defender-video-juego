import esper
import pygame
import pytest

from src.ecs.components.c_player_state import CPlayerState, FacingDirection, VerticalDirection
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.systems.s_player_state import system_player_state


PLAYER_CFG = {
    "image": "",
    "acceleration": 100,
    "deceleration": 50,
    "reverse_deceleration": 200,
    "max_speed": 80,
    "vertical_speed": 60,
    "initial_position": pygame.Vector2(0, 0),
    "animations": {}
}


def _create_player(world):
    entity = world.create_entity()
    world.add_component(entity, CPlayerState())
    world.add_component(entity, CVelocity(pygame.Vector2(0, 0)))
    world.add_component(entity, CSurface(pygame.Vector2(10, 10), pygame.Color(255, 255, 255)))
    return entity


class TestAcceleration:
    def setup_method(self):
        self.world = esper.World()
        self.entity = _create_player(self.world)

    def test_thrust_increases_velocity(self):
        state = self.world.component_for_entity(self.entity, CPlayerState)
        state.moving_horizontal = True
        state.facing = FacingDirection.RIGHT

        system_player_state(self.world, 1.0, PLAYER_CFG)

        vel = self.world.component_for_entity(self.entity, CVelocity).vel
        assert vel.x == pytest.approx(80)  # capped at max_speed

    def test_thrust_accelerates_gradually(self):
        state = self.world.component_for_entity(self.entity, CPlayerState)
        state.moving_horizontal = True
        state.facing = FacingDirection.RIGHT

        system_player_state(self.world, 0.1, PLAYER_CFG)

        vel = self.world.component_for_entity(self.entity, CVelocity).vel
        assert vel.x == pytest.approx(10)  # 100 * 0.1

    def test_velocity_capped_at_max_speed(self):
        state = self.world.component_for_entity(self.entity, CPlayerState)
        state.moving_horizontal = True
        state.facing = FacingDirection.RIGHT

        for _ in range(10):
            system_player_state(self.world, 1.0, PLAYER_CFG)

        vel = self.world.component_for_entity(self.entity, CVelocity).vel
        assert vel.x == pytest.approx(80)

    def test_thrust_left_produces_negative_velocity(self):
        state = self.world.component_for_entity(self.entity, CPlayerState)
        state.moving_horizontal = True
        state.facing = FacingDirection.LEFT

        system_player_state(self.world, 0.1, PLAYER_CFG)

        vel = self.world.component_for_entity(self.entity, CVelocity).vel
        assert vel.x == pytest.approx(-10)


class TestDeceleration:
    def setup_method(self):
        self.world = esper.World()
        self.entity = _create_player(self.world)

    def test_release_key_decelerates(self):
        vel = self.world.component_for_entity(self.entity, CVelocity)
        vel.vel.x = 80
        state = self.world.component_for_entity(self.entity, CPlayerState)
        state.moving_horizontal = False

        system_player_state(self.world, 1.0, PLAYER_CFG)

        assert vel.vel.x == pytest.approx(30)  # 80 - 50*1.0

    def test_deceleration_stops_at_zero(self):
        vel = self.world.component_for_entity(self.entity, CVelocity)
        vel.vel.x = 10
        state = self.world.component_for_entity(self.entity, CPlayerState)
        state.moving_horizontal = False

        system_player_state(self.world, 1.0, PLAYER_CFG)

        assert vel.vel.x == pytest.approx(0)

    def test_reverse_deceleration_is_faster(self):
        vel = self.world.component_for_entity(self.entity, CVelocity)
        vel.vel.x = 80  # moving right
        state = self.world.component_for_entity(self.entity, CPlayerState)
        state.moving_horizontal = True
        state.facing = FacingDirection.LEFT  # wants to go left

        system_player_state(self.world, 0.1, PLAYER_CFG)

        # reverse_deceleration = 200, so 80 - 200*0.1 = 60
        assert vel.vel.x == pytest.approx(60)

    def test_reverse_then_accelerates_in_new_direction(self):
        vel = self.world.component_for_entity(self.entity, CVelocity)
        vel.vel.x = 10  # small rightward velocity
        state = self.world.component_for_entity(self.entity, CPlayerState)
        state.moving_horizontal = True
        state.facing = FacingDirection.LEFT

        # First call: decelerate (10 - 200*0.1 = -10 -> clamped to 0)
        system_player_state(self.world, 0.1, PLAYER_CFG)
        assert vel.vel.x == pytest.approx(0)

        # Second call: now accelerate left (0 + 100*-1*0.1 = -10)
        system_player_state(self.world, 0.1, PLAYER_CFG)
        assert vel.vel.x == pytest.approx(-10)


class TestVerticalMovement:
    def setup_method(self):
        self.world = esper.World()
        self.entity = _create_player(self.world)

    def test_move_up(self):
        state = self.world.component_for_entity(self.entity, CPlayerState)
        state.vertical = VerticalDirection.UP

        system_player_state(self.world, 1.0, PLAYER_CFG)

        vel = self.world.component_for_entity(self.entity, CVelocity).vel
        assert vel.y == pytest.approx(-60)

    def test_move_down(self):
        state = self.world.component_for_entity(self.entity, CPlayerState)
        state.vertical = VerticalDirection.DOWN

        system_player_state(self.world, 1.0, PLAYER_CFG)

        vel = self.world.component_for_entity(self.entity, CVelocity).vel
        assert vel.y == pytest.approx(60)

    def test_vertical_none_stops(self):
        vel = self.world.component_for_entity(self.entity, CVelocity)
        vel.vel.y = 60
        state = self.world.component_for_entity(self.entity, CPlayerState)
        state.vertical = VerticalDirection.NONE

        system_player_state(self.world, 1.0, PLAYER_CFG)

        assert vel.vel.y == pytest.approx(0)
