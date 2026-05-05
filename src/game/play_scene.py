import pygame

from src.engine.scenes.scene import Scene
from src.ecs.load.load_world import load_world_config
from src.create.prefab_creator import create_star
from src.ecs.systems.s_star_blink import system_star_blink
from src.ecs.systems.s_rendering import system_rendering


class PlayScene(Scene):

    def do_create(self):
        self._world_cfg = load_world_config("assets/cfg/world.json")

        for _ in range(self._world_cfg["stars_number"]):
            create_star(
                self.ecs_world,
                self.screen_rect,
                self._world_cfg["star_colors"],
                self._world_cfg["stars_blink_rate"]
            )

    def do_process_events(self, event: pygame.event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.switch_scene("GAME_OVER_SCENE")

    def do_update(self, delta_time: float):
        system_star_blink(self.ecs_world, delta_time)

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)
