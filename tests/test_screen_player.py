import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.systems.s_screen_player import system_screen_player


SCREEN_RECT = pygame.Rect(0, 0, 320, 256)
WORLD_WIDTH = 3200


def _create_player(world, x, y, w=10, h=10):
    entity = world.create_entity()
    world.add_component(entity, CTransform(pygame.Vector2(x, y)))
    world.add_component(entity, CSurface(pygame.Vector2(w, h), pygame.Color(255, 255, 255)))
    world.add_component(entity, CTagPlayer())
    return entity


class TestScreenPlayerVertical:
    def setup_method(self):
        self.world = esper.World()

    def test_clamps_top_edge(self):
        entity = _create_player(self.world, 100, -5)
        system_screen_player(self.world, SCREEN_RECT, WORLD_WIDTH)
        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.y == 0

    def test_clamps_bottom_edge(self):
        entity = _create_player(self.world, 100, 250)
        system_screen_player(self.world, SCREEN_RECT, WORLD_WIDTH)
        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.y == 246  # 256 - 10

    def test_inside_bounds_unchanged(self):
        entity = _create_player(self.world, 100, 100)
        system_screen_player(self.world, SCREEN_RECT, WORLD_WIDTH)
        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.y == 100


class TestScreenPlayerHorizontalWrap:
    def setup_method(self):
        self.world = esper.World()

    def test_wraps_past_world_width(self):
        entity = _create_player(self.world, 3250, 100)
        system_screen_player(self.world, SCREEN_RECT, WORLD_WIDTH)
        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.x == 50  # 3250 % 3200

    def test_wraps_negative_position(self):
        entity = _create_player(self.world, -50, 100)
        system_screen_player(self.world, SCREEN_RECT, WORLD_WIDTH)
        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.x == 3150  # -50 % 3200

    def test_no_wrap_within_bounds(self):
        entity = _create_player(self.world, 1500, 100)
        system_screen_player(self.world, SCREEN_RECT, WORLD_WIDTH)
        pos = self.world.component_for_entity(entity, CTransform).pos
        assert pos.x == 1500
