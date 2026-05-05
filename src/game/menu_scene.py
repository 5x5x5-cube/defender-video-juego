import pygame

from src.engine.scenes.scene import Scene
from src.engine.service_locator import ServiceLocator
from src.ecs.load.load_world import load_interface_config
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.systems.s_rendering import system_rendering


class MenuScene(Scene):

    def do_create(self):
        self._interface_cfg = load_interface_config("assets/cfg/interface.json")

        logo_surf = ServiceLocator.images_service.get("assets/img/game_logo.png")
        logo_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(logo_entity, CSurface.from_surface(logo_surf))
        logo_rect = logo_surf.get_rect()
        self.ecs_world.add_component(logo_entity, CTransform(pygame.Vector2(
            self.screen_rect.centerx - logo_rect.width // 2,
            self.screen_rect.centery - 40 - logo_rect.height // 2
        )))

        font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", 8)
        text_surf = font.render(
            "PRESS ENTER TO START",
            False,
            self._interface_cfg["normal_text_color"]
        )
        text_entity = self.ecs_world.create_entity()
        self.ecs_world.add_component(text_entity, CSurface.from_surface(text_surf))
        text_rect = text_surf.get_rect()
        self.ecs_world.add_component(text_entity, CTransform(pygame.Vector2(
            self.screen_rect.centerx - text_rect.width // 2,
            self.screen_rect.centery + 30
        )))

    def do_process_events(self, event: pygame.event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.switch_scene("PLAY_SCENE")

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)
