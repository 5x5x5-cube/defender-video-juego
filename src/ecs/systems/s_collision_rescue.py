import esper

from src.ecs.components.c_humanoid_state import CHumanoidState, HumanoidState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_humanoid import CTagHumanoid
from src.ecs.components.tags.c_tag_player import CTagPlayer
import src.engine.game_state as game_state

RESCUE_SCORE = 500


def system_collision_rescue(world: esper.World):
    player_data = _get_player_data(world)
    if player_data is None:
        return

    player_rect = player_data

    for humanoid_entity, (c_transform, c_velocity, c_surface, c_humanoid_state, _) in world.get_components(
            CTransform, CVelocity, CSurface, CHumanoidState, CTagHumanoid):
        if c_humanoid_state.state != HumanoidState.FALLING:
            continue

        humanoid_rect = c_surface.get_area_relative(c_transform.pos)
        if player_rect.colliderect(humanoid_rect):
            c_velocity.vel.y = 0
            c_transform.pos.y = c_humanoid_state.spawn_y
            c_humanoid_state.spawn_x = c_transform.pos.x
            c_humanoid_state.state = HumanoidState.ON_GROUND
            game_state.score += RESCUE_SCORE


def _get_player_data(world: esper.World):
    for _, (c_transform, c_surface, _) in world.get_components(
            CTransform, CSurface, CTagPlayer):
        return c_surface.get_area_relative(c_transform.pos)
    return None
