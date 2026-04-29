import asyncio
import pygame
import esper

from src.ecs.load.load_world import load_window_config


class GameEngine:
    def __init__(self) -> None:
        pygame.init()
        self.window_config = load_window_config("assets/cfg/window.json")
        self.screen = pygame.display.set_mode(self.window_config["size"], 0)
        pygame.display.set_caption(self.window_config["title"])
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        self.game_time = 0
        self.is_running = False

        self.ecs_world = esper.World()

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        pass

    def _calculate_time(self):
        self.clock.tick(self.window_config["framerate"])
        self.delta_time = self.clock.get_time() / 1000.0
        self.game_time += self.delta_time

    def _process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        pass

    def _draw(self):
        self.screen.fill(self.window_config["bg_color"])
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
