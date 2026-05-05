import esper
import pygame
import pytest

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_star_blink import CStarBlink
from src.ecs.systems.s_star_blink import system_star_blink


class TestStarBlink:
    def setup_method(self):
        self.world = esper.World()

    def _create_star(self, rate=0.5):
        color = pygame.Color(255, 0, 0)
        entity = self.world.create_entity()
        self.world.add_component(entity, CTransform(pygame.Vector2(0, 0)))
        self.world.add_component(entity, CSurface(pygame.Vector2(1, 1), color))
        self.world.add_component(entity, CStarBlink(rate, color))
        return entity

    def test_star_starts_visible(self):
        entity = self._create_star()
        blink = self.world.component_for_entity(entity, CStarBlink)
        assert blink.visible is True

    def test_star_toggles_off_after_rate(self):
        entity = self._create_star(rate=0.5)

        system_star_blink(self.world, 0.5)

        blink = self.world.component_for_entity(entity, CStarBlink)
        assert blink.visible is False

    def test_star_toggles_back_on(self):
        entity = self._create_star(rate=0.5)

        system_star_blink(self.world, 0.5)  # off
        system_star_blink(self.world, 0.5)  # on

        blink = self.world.component_for_entity(entity, CStarBlink)
        assert blink.visible is True

    def test_star_stays_visible_before_rate(self):
        entity = self._create_star(rate=0.5)

        system_star_blink(self.world, 0.3)

        blink = self.world.component_for_entity(entity, CStarBlink)
        assert blink.visible is True

    def test_surface_cleared_when_hidden(self):
        entity = self._create_star(rate=0.5)

        system_star_blink(self.world, 0.5)

        surface = self.world.component_for_entity(entity, CSurface)
        pixel_color = surface.surf.get_at((0, 0))
        assert pixel_color.a == 0

    def test_surface_restored_when_visible(self):
        entity = self._create_star(rate=0.5)

        system_star_blink(self.world, 0.5)  # off
        system_star_blink(self.world, 0.5)  # on

        surface = self.world.component_for_entity(entity, CSurface)
        pixel_color = surface.surf.get_at((0, 0))
        assert pixel_color.r == 255
