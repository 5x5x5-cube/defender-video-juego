import pygame
import esper

import src.engine.game_engine

class Scene:
    def __init__(self, game_engine:'src.engine.game_engine.GameEngine') -> None:
        self.ecs_world = esper.World()
        self._game_engine:src.engine.game_engine.GameEngine = game_engine
        self.screen_rect = self._game_engine.screen.get_rect()

    def do_process_events(self, event:pygame.event):
        pass

    def simulate(self, delta_time):
        self.do_update(delta_time)
        self.ecs_world._clear_dead_entities()

    def clean(self):
        self.ecs_world.clear_database()
        self.do_clean()

    def switch_scene(self, new_scene_name:str):
        self._game_engine.switch_scene(new_scene_name)

    def do_create(self):
        pass

    def do_update(self, delta_time:float):
        pass

    def do_draw(self, screen):
        pass

    def do_action(self, action):
        pass

    def do_clean(self):
        pass
