import pygame

from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.ecs.load.load_world import load_interface_config
import src.engine.game_state as game_state

_AUTO_ADVANCE_DELAY = 4.0
_BLINK_RATE = 0.5


class WaveCompleteScene(Scene):

    def do_create(self):
        self._interface_cfg = load_interface_config("assets/cfg/interface.json")
        self._timer = 0.0
        self._blink_timer = 0.0
        self._show_prompt = True

        font_big = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 16)
        font_mid = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 10)
        font_small = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)

        wave_label = f"WAVE {game_state.current_wave} COMPLETE!"
        self._wave_text = font_big.render(
            wave_label, False, pygame.Color(255, 220, 0))
        self._wave_rect = self._wave_text.get_rect(
            centerx=self.screen_rect.centerx,
            centery=self.screen_rect.centery - 40)

        next_label = f"NEXT: WAVE {game_state.current_wave + 1}"
        self._next_text = font_mid.render(
            next_label, False, self._interface_cfg["normal_text_color"])
        self._next_rect = self._next_text.get_rect(
            centerx=self.screen_rect.centerx,
            centery=self.screen_rect.centery)

        score_str = f"SCORE  {str(game_state.score).zfill(6)}"
        self._score_text = font_mid.render(
            score_str, False, self._interface_cfg["normal_text_color"])
        self._score_rect = self._score_text.get_rect(
            centerx=self.screen_rect.centerx,
            centery=self.screen_rect.centery + 22)

        self._prompt_text = font_small.render(
            "PRESS ENTER TO CONTINUE",
            False, self._interface_cfg["normal_text_color"])
        self._prompt_rect = self._prompt_text.get_rect(
            centerx=self.screen_rect.centerx,
            centery=self.screen_rect.centery + 50)

    def do_process_events(self, event: pygame.event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self._advance()

    def do_update(self, delta_time: float):
        self._timer += delta_time
        self._blink_timer += delta_time
        if self._blink_timer >= _BLINK_RATE:
            self._blink_timer = 0.0
            self._show_prompt = not self._show_prompt
        if self._timer >= _AUTO_ADVANCE_DELAY:
            self._advance()

    def do_draw(self, screen):
        screen.blit(self._wave_text, self._wave_rect)
        screen.blit(self._next_text, self._next_rect)
        screen.blit(self._score_text, self._score_rect)
        if self._show_prompt:
            screen.blit(self._prompt_text, self._prompt_rect)

    def _advance(self):
        self.switch_scene("PLAY_SCENE")
