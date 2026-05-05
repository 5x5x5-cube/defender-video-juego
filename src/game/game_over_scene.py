import pygame

from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.ecs.load.load_world import load_interface_config


class GameOverScene(Scene):

    def do_create(self):
        self._interface_cfg = load_interface_config("assets/cfg/interface.json")

        font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 16)
        self._game_over_text = font.render(
            "GAME OVER",
            False,
            self._interface_cfg["title_text_color"]
        )
        self._game_over_rect = self._game_over_text.get_rect(
            centerx=self.screen_rect.centerx,
            centery=self.screen_rect.centery - 20
        )

        small_font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)
        self._restart_text = small_font.render(
            "PRESS ENTER TO RESTART",
            False,
            self._interface_cfg["normal_text_color"]
        )
        self._restart_rect = self._restart_text.get_rect(
            centerx=self.screen_rect.centerx,
            centery=self.screen_rect.centery + 20
        )

        self._menu_text = small_font.render(
            "PRESS ESC FOR MENU",
            False,
            self._interface_cfg["normal_text_color"]
        )
        self._menu_rect = self._menu_text.get_rect(
            centerx=self.screen_rect.centerx,
            centery=self.screen_rect.centery + 40
        )

    def do_process_events(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.switch_scene("PLAY_SCENE")
            elif event.key == pygame.K_ESCAPE:
                self.switch_scene("MENU_SCENE")

    def do_draw(self, screen):
        screen.blit(self._game_over_text, self._game_over_rect)
        screen.blit(self._restart_text, self._restart_rect)
        screen.blit(self._menu_text, self._menu_rect)
