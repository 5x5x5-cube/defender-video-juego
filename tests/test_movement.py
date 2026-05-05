import esper
import pygame
import pytest

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement


class TestMovement:
    def setup_method(self):
        self.world = esper.World()

    def test_entity_moves_by_velocity(self):
        entity = self.world.create_entity()
        self.world.add_component(entity, CTransform(pygame.Vector2(0, 0)))
        self.world.add_component(entity, CVelocity(pygame.Vector2(100, 0)))

        system_movement(self.world, 1.0)

        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.x == 100
        assert pos.y == 0

    def test_movement_scales_with_delta_time(self):
        entity = self.world.create_entity()
        self.world.add_component(entity, CTransform(pygame.Vector2(0, 0)))
        self.world.add_component(entity, CVelocity(pygame.Vector2(100, 0)))

        system_movement(self.world, 0.5)

        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.x == 50

    def test_negative_velocity_moves_left(self):
        entity = self.world.create_entity()
        self.world.add_component(entity, CTransform(pygame.Vector2(100, 0)))
        self.world.add_component(entity, CVelocity(pygame.Vector2(-50, 0)))

        system_movement(self.world, 1.0)

        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.x == 50

    def test_zero_velocity_no_movement(self):
        entity = self.world.create_entity()
        self.world.add_component(entity, CTransform(pygame.Vector2(10, 20)))
        self.world.add_component(entity, CVelocity(pygame.Vector2(0, 0)))

        system_movement(self.world, 1.0)

        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.x == 10
        assert pos.y == 20
