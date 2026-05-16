import pygame

from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.ecs.load.load_world import load_interface_config
import src.engine.game_state as game_state


class WinScene(Scene):

    def do_create(self):
        self._interface_cfg = load_interface_config("assets/cfg/interface.json")
        self._blink_timer = 0.0
        self._show_prompt = True

        font_big = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 16)
        font_mid = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 10)
        font_small = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)

        self._win_text = font_big.render(
            "YOU WIN!", False, pygame.Color(0, 255, 128))
        self._win_rect = self._win_text.get_rect(
            centerx=self.screen_rect.centerx,
            centery=self.screen_rect.centery - 40)

        score_str = f"SCORE  {str(game_state.score).zfill(6)}"
        self._score_text = font_mid.render(
            score_str, False, self._interface_cfg["normal_text_color"])
        self._score_rect = self._score_text.get_rect(
            centerx=self.screen_rect.centerx,
            centery=self.screen_rect.centery)

        self._prompt_text = font_small.render(
            "PRESS ENTER TO PLAY AGAIN",
            False, self._interface_cfg["normal_text_color"])
        self._prompt_rect = self._prompt_text.get_rect(
            centerx=self.screen_rect.centerx,
            centery=self.screen_rect.centery + 40)

        self._menu_text = font_small.render(
            "PRESS ESC FOR MENU",
            False, self._interface_cfg["normal_text_color"])
        self._menu_rect = self._menu_text.get_rect(
            centerx=self.screen_rect.centerx,
            centery=self.screen_rect.centery + 60)

    def do_process_events(self, event: pygame.event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                game_state.reset()
                self.switch_scene("PLAY_SCENE")
            elif event.key == pygame.K_ESCAPE:
                game_state.reset()
                self.switch_scene("MENU_SCENE")

    def do_update(self, delta_time: float):
        self._blink_timer += delta_time
        if self._blink_timer >= 0.5:
            self._blink_timer = 0.0
            self._show_prompt = not self._show_prompt

    def do_draw(self, screen):
        screen.blit(self._win_text, self._win_rect)
        screen.blit(self._score_text, self._score_rect)
        if self._show_prompt:
            screen.blit(self._prompt_text, self._prompt_rect)
        screen.blit(self._menu_text, self._menu_rect)
