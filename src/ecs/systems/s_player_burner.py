import esper
import pygame

from src.ecs.components.c_player_state import CPlayerState, FacingDirection
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.components.tags.c_tag_player_burner import CTagPlayerBurner
from src.engine.service_locator import ServiceLocator
from src.ecs.load.load_world import PlayerConfig


def system_player_burner(world: esper.World, player_cfg: PlayerConfig):
    player_pos, player_state, player_surface = _get_player_data(world)
    if player_pos is None:
        return

    for _, (c_transform, c_surface, _) in world.get_components(
            CTransform, CSurface, CTagPlayerBurner):
        _update_burner_sprite(c_surface, player_state, player_cfg)
        _update_burner_position(c_transform, c_surface, player_pos,
                                player_surface, player_state)


def _get_player_data(world: esper.World):
    for _, (c_transform, c_player_state, c_surface) in world.get_components(
            CTransform, CPlayerState, CSurface):
        return c_transform, c_player_state, c_surface
    return None, None, None


def _update_burner_sprite(c_surface: CSurface, player_state: CPlayerState,
                          player_cfg: PlayerConfig):
    if player_state.moving_horizontal:
        new_surf = ServiceLocator.images_service.get(player_cfg["burner_moving_image"])
    else:
        new_surf = ServiceLocator.images_service.get(player_cfg["burner_idle_image"])

    if player_state.facing == FacingDirection.LEFT:
        new_surf = pygame.transform.flip(new_surf, True, False)

    c_surface.surf = new_surf
    c_surface.area = new_surf.get_rect()


def _update_burner_position(c_transform: CTransform, c_surface: CSurface,
                            player_pos: CTransform, player_surface: CSurface,
                            player_state: CPlayerState):
    player_rect = player_surface.area
    burner_rect = c_surface.area

    if player_state.facing == FacingDirection.RIGHT:
        c_transform.pos.x = player_pos.pos.x - burner_rect.width
    else:
        c_transform.pos.x = player_pos.pos.x + player_rect.width

    c_transform.pos.y = player_pos.pos.y
