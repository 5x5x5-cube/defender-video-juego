import pygame

from src.engine.scenes.scene import Scene


class ExampleScene2(Scene):

    def do_create(self):
        font = pygame.font.SysFont(None, 36)
        self._title_surf = font.render("Example Scene 2 (Press Z for Scene 1)", True, pygame.Color(50, 255, 50))
        self._title_pos = self._title_surf.get_rect(center=(self.screen_rect.centerx, self.screen_rect.centery))

    def do_process_events(self, event: pygame.event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
            self.switch_scene("EXAMPLE_SCENE")

    def do_draw(self, screen):
        screen.blit(self._title_surf, self._title_pos)
