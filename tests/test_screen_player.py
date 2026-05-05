import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_screen_player import system_screen_player


SCREEN_RECT = pygame.Rect(0, 0, 320, 256)


def _create_player(world, x, y, w=10, h=10):
    entity = world.create_entity()
    world.add_component(entity, CTransform(pygame.Vector2(x, y)))
    world.add_component(entity, CSurface(pygame.Vector2(w, h), pygame.Color(255, 255, 255)))
    world.add_component(entity, CTagPlayer())
    return entity


class TestScreenPlayer:
    def setup_method(self):
        self.world = esper.World()

    def test_clamps_left_edge(self):
        entity = _create_player(self.world, -5, 100)
        system_screen_player(self.world, SCREEN_RECT)
        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.x == 0

    def test_clamps_right_edge(self):
        entity = _create_player(self.world, 315, 100)
        system_screen_player(self.world, SCREEN_RECT)
        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.x == 310  # 320 - 10

    def test_clamps_top_edge(self):
        entity = _create_player(self.world, 100, -5)
        system_screen_player(self.world, SCREEN_RECT)
        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.y == 0

    def test_clamps_bottom_edge(self):
        entity = _create_player(self.world, 100, 250)
        system_screen_player(self.world, SCREEN_RECT)
        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.y == 246  # 256 - 10

    def test_inside_bounds_unchanged(self):
        entity = _create_player(self.world, 100, 100)
        system_screen_player(self.world, SCREEN_RECT)
        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.x == 100
        assert pos.y == 100
