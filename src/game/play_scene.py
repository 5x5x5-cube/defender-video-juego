import pygame

from src.engine.scenes.scene import Scene
from src.ecs.load.load_world import load_world_config, load_player_config
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_player_state import CPlayerState, FacingDirection, VerticalDirection
from src.create.prefab_creator import create_star, create_player, create_player_burner, create_input_commands
from src.ecs.systems.s_star_blink import system_star_blink
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_screen_player import system_screen_player
from src.ecs.systems.s_player_burner import system_player_burner


class PlayScene(Scene):

    def do_create(self):
        self._world_cfg = load_world_config("assets/cfg/world.json")
        self._player_cfg = load_player_config("assets/cfg/player.json")

        for _ in range(self._world_cfg["stars_number"]):
            create_star(
                self.ecs_world,
                self.screen_rect,
                self._world_cfg["star_colors"],
                self._world_cfg["stars_blink_rate"]
            )

        create_player(self.ecs_world, self._player_cfg)
        create_player_burner(self.ecs_world, self._player_cfg,
                             self._player_cfg["initial_position"])
        create_input_commands(self.ecs_world)
        self._held_horizontal: set[FacingDirection] = set()

    def do_process_events(self, event: pygame.event):
        system_input_player(self.ecs_world, event, self.do_action)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.switch_scene("GAME_OVER_SCENE")

    def do_action(self, c_input: CInputCommand):
        if c_input.name == "MOVE_RIGHT":
            self._set_player_horizontal(
                FacingDirection.RIGHT, c_input.phase == CommandPhase.START)
        elif c_input.name == "MOVE_LEFT":
            self._set_player_horizontal(
                FacingDirection.LEFT, c_input.phase == CommandPhase.START)
        elif c_input.name == "MOVE_UP":
            self._set_player_vertical(
                VerticalDirection.UP if c_input.phase == CommandPhase.START
                else VerticalDirection.NONE)
        elif c_input.name == "MOVE_DOWN":
            self._set_player_vertical(
                VerticalDirection.DOWN if c_input.phase == CommandPhase.START
                else VerticalDirection.NONE)

    def do_update(self, delta_time: float):
        system_player_state(self.ecs_world, delta_time, self._player_cfg)
        system_movement(self.ecs_world, delta_time)
        system_screen_player(self.ecs_world, self.screen_rect)
        system_player_burner(self.ecs_world, self._player_cfg)
        system_star_blink(self.ecs_world, delta_time)

    def do_draw(self, screen):
        system_rendering(self.ecs_world, screen)

    def _set_player_horizontal(self, direction: FacingDirection, pressed: bool):
        if pressed:
            self._held_horizontal.add(direction)
        else:
            self._held_horizontal.discard(direction)

        for _, c_player_state in self.ecs_world.get_component(CPlayerState):
            if not self._held_horizontal:
                c_player_state.moving_horizontal = False
            elif c_player_state.moving_horizontal:
                if direction not in self._held_horizontal:
                    c_player_state.facing = next(iter(self._held_horizontal))
            else:
                c_player_state.moving_horizontal = True
                c_player_state.facing = direction

    def _set_player_vertical(self, direction: VerticalDirection):
        for _, c_player_state in self.ecs_world.get_component(CPlayerState):
            c_player_state.vertical = direction
