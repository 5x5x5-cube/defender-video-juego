import esper
import pygame

from src.ecs.components.c_player_state import CPlayerState, FacingDirection, VerticalDirection
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.load.load_world import PlayerConfig


def system_player_state(world: esper.World, delta_time: float,
                        player_cfg: PlayerConfig):
    for _, (c_player_state, c_velocity, c_surface) in world.get_components(
            CPlayerState, CVelocity, CSurface):
        _handle_horizontal(c_player_state, c_velocity, delta_time, player_cfg)
        _handle_vertical(c_player_state, c_velocity, player_cfg)
        _handle_sprite_flip(c_player_state, c_surface)


def _handle_horizontal(c_player_state: CPlayerState, c_velocity: CVelocity,
                       delta_time: float, player_cfg: PlayerConfig):
    if not c_player_state.moving_horizontal:
        _apply_deceleration(c_velocity, delta_time, player_cfg["deceleration"])
        return

    direction = c_player_state.facing.value
    moving_against = (c_velocity.vel.x > 0 and direction < 0) or \
                     (c_velocity.vel.x < 0 and direction > 0)

    if moving_against:
        _apply_deceleration(c_velocity, delta_time, player_cfg["reverse_deceleration"])
    else:
        _apply_acceleration(c_player_state, c_velocity, delta_time, player_cfg)


def _apply_acceleration(c_player_state: CPlayerState, c_velocity: CVelocity,
                        delta_time: float, player_cfg: PlayerConfig):
    direction = c_player_state.facing.value
    max_speed = player_cfg["max_speed"]
    c_velocity.vel.x += player_cfg["acceleration"] * direction * delta_time
    if abs(c_velocity.vel.x) > max_speed:
        c_velocity.vel.x = max_speed * direction


def _apply_deceleration(c_velocity: CVelocity, delta_time: float,
                        deceleration: float):
    if c_velocity.vel.x > 0:
        c_velocity.vel.x -= deceleration * delta_time
        if c_velocity.vel.x < 0:
            c_velocity.vel.x = 0
    elif c_velocity.vel.x < 0:
        c_velocity.vel.x += deceleration * delta_time
        if c_velocity.vel.x > 0:
            c_velocity.vel.x = 0


def _handle_vertical(c_player_state: CPlayerState, c_velocity: CVelocity,
                     player_cfg: PlayerConfig):
    if c_player_state.vertical == VerticalDirection.NONE:
        c_velocity.vel.y = 0
    else:
        c_velocity.vel.y = player_cfg["vertical_speed"] * c_player_state.vertical.value


def _handle_sprite_flip(c_player_state: CPlayerState, c_surface: CSurface):
    if c_player_state.facing == FacingDirection.LEFT:
        if not getattr(c_surface, '_flipped', False):
            c_surface.surf = pygame.transform.flip(c_surface.surf, True, False)
            c_surface._flipped = True
    else:
        if getattr(c_surface, '_flipped', False):
            c_surface.surf = pygame.transform.flip(c_surface.surf, True, False)
            c_surface._flipped = False
