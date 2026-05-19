from typing import Callable

import esper
import pygame

from src.ecs.components.c_input_command import CInputCommand, CommandPhase


def system_input_player(world: esper.World, event: pygame.Event,
                        do_action: Callable[[CInputCommand], None]):
    for _, c_input in world.get_component(CInputCommand):
        if event.type == pygame.KEYDOWN and event.key == c_input.key:
            c_input.phase = CommandPhase.START
            do_action(c_input)
        elif event.type == pygame.KEYUP and event.key == c_input.key:
            c_input.phase = CommandPhase.END
            do_action(c_input)
