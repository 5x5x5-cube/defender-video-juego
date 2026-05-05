import esper

from src.ecs.components.c_player_state import CPlayerState, FacingDirection
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_player_burner import CTagPlayerBurner


def system_player_burner_tracking(world: esper.World):
    player_pos, player_state, player_surface = _get_player_data(world)
    if player_pos is None:
        return

    for _, (c_transform, c_surface, _) in world.get_components(
            CTransform, CSurface, CTagPlayerBurner):
        _sync_position(c_transform, c_surface, player_pos,
                       player_surface, player_state)


def _get_player_data(world: esper.World):
    for _, (c_transform, c_player_state, c_surface) in world.get_components(
            CTransform, CPlayerState, CSurface):
        return c_transform, c_player_state, c_surface
    return None, None, None


def _sync_position(c_transform: CTransform, c_surface: CSurface,
                   player_pos: CTransform, player_surface: CSurface,
                   player_state: CPlayerState):
    player_rect = player_surface.area
    burner_frame_width = c_surface.area.width

    overlap = 2
    if player_state.facing == FacingDirection.RIGHT:
        c_transform.pos.x = player_pos.pos.x - burner_frame_width + overlap
    else:
        c_transform.pos.x = player_pos.pos.x + player_rect.width - overlap

    burner_height = c_surface.area.height
    c_transform.pos.y = player_pos.pos.y + (player_rect.height - burner_height) // 2
