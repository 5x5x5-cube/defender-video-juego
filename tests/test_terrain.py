import esper
import pygame

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_parallax import CParallax
from src.create.prefab_creator import create_terrain, _generate_terrain_points


WORLD_WIDTH = 3200
SCREEN_HEIGHT = 256
NUM_POINTS = 50
COLOR = pygame.Color(255, 90, 90)
BG_COLOR = pygame.Color(25, 25, 25)
PARALLAX = 1.25


class TestTerrainGeneration:
    def test_first_and_last_point_same_y(self):
        terrain_width = int(WORLD_WIDTH * PARALLAX)
        points = _generate_terrain_points(terrain_width, SCREEN_HEIGHT, NUM_POINTS)
        assert points[0][1] == points[-1][1]

    def test_first_point_at_x_zero(self):
        terrain_width = int(WORLD_WIDTH * PARALLAX)
        points = _generate_terrain_points(terrain_width, SCREEN_HEIGHT, NUM_POINTS)
        assert points[0][0] == 0

    def test_last_point_at_world_width(self):
        terrain_width = int(WORLD_WIDTH * PARALLAX)
        points = _generate_terrain_points(terrain_width, SCREEN_HEIGHT, NUM_POINTS)
        assert points[-1][0] == terrain_width

    def test_points_within_height_bounds(self):
        terrain_width = int(WORLD_WIDTH * PARALLAX)
        points = _generate_terrain_points(terrain_width, SCREEN_HEIGHT, NUM_POINTS)
        min_y = int(SCREEN_HEIGHT * 0.75)
        max_y = SCREEN_HEIGHT - 5
        for _, y in points:
            assert min_y <= y <= max_y

    def test_correct_number_of_points(self):
        terrain_width = int(WORLD_WIDTH * PARALLAX)
        points = _generate_terrain_points(terrain_width, SCREEN_HEIGHT, NUM_POINTS)
        assert len(points) == NUM_POINTS


class TestTerrainEntity:
    def setup_method(self):
        self.world = esper.World()

    def test_creates_entity_with_components(self):
        create_terrain(self.world, WORLD_WIDTH, SCREEN_HEIGHT,
                       NUM_POINTS, COLOR, BG_COLOR, PARALLAX)

        entities = self.world.get_components(CTransform, CSurface, CParallax)
        assert len(entities) == 1

    def test_surface_width_matches_parallax_world(self):
        create_terrain(self.world, WORLD_WIDTH, SCREEN_HEIGHT,
                       NUM_POINTS, COLOR, BG_COLOR, PARALLAX)

        for _, (_, c_surface, _) in self.world.get_components(
                CTransform, CSurface, CParallax):
            assert c_surface.surf.get_width() == int(WORLD_WIDTH * PARALLAX)

    def test_parallax_factor_set(self):
        create_terrain(self.world, WORLD_WIDTH, SCREEN_HEIGHT,
                       NUM_POINTS, COLOR, BG_COLOR, PARALLAX)

        for _, (_, _, c_parallax) in self.world.get_components(
                CTransform, CSurface, CParallax):
            assert c_parallax.factor == PARALLAX

    def test_positioned_at_origin(self):
        create_terrain(self.world, WORLD_WIDTH, SCREEN_HEIGHT,
                       NUM_POINTS, COLOR, BG_COLOR, PARALLAX)

        for _, (c_transform, _, _) in self.world.get_components(
                CTransform, CSurface, CParallax):
            assert c_transform.pos.x == 0
            assert c_transform.pos.y == 0
