import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_player_state import CPlayerState, FacingDirection
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player_burner import CTagPlayerBurner
from src.engine.service_locator import ServiceLocator
from src.ecs.load.load_world import PlayerConfig


def system_player_burner_state(world: esper.World, player_cfg: PlayerConfig):
    player_state = _get_player_state(world)
    if player_state is None:
        return

    burner_cfg = player_cfg["animations"]["burner"]
    anim_cfg = burner_cfg["moving"] if player_state.moving_horizontal else burner_cfg["idle"]
    expected_surf = ServiceLocator.images_service.get(anim_cfg["image"])

    for burner_entity, (c_surface, _, _) in world.get_components(
            CSurface, CAnimation, CTagPlayerBurner):
        if c_surface.surf.get_size() != expected_surf.get_size():
            _swap_spritesheet(world, burner_entity, c_surface, expected_surf, anim_cfg)
        _apply_facing_flip(c_surface, player_state, expected_surf)


def _get_player_state(world: esper.World):
    for _, c_player_state in world.get_component(CPlayerState):
        return c_player_state
    return None


def _swap_spritesheet(world: esper.World, burner_entity: int,
                      c_surface: CSurface, new_surf: pygame.Surface,
                      anim_cfg: dict):
    c_surface.surf = new_surf
    frame_width = new_surf.get_width() // anim_cfg["number_frames"]
    c_surface.area = pygame.Rect(0, 0, frame_width, new_surf.get_height())
    world.add_component(burner_entity,
                        CAnimation(anim_cfg["number_frames"], anim_cfg["list"]))


def _apply_facing_flip(c_surface: CSurface, player_state: CPlayerState,
                       original_surf: pygame.Surface):
    if player_state.facing == FacingDirection.LEFT:
        c_surface.surf = pygame.transform.flip(original_surf, True, False)
    else:
        c_surface.surf = original_surf
