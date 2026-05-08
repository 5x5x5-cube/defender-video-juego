import esper

from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_shoot_timer import CShootTimer
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.ecs.load.load_world import LanderConfig
from src.create.prefab_creator import create_enemy_bullet


def system_enemy_shooting(world: esper.World, delta_time: float,
                          lander_cfg: LanderConfig):
    player_pos = _get_player_position(world)
    c_viewport = _get_viewport(world)
    if player_pos is None or c_viewport is None:
        return

    for _, (c_transform, c_shoot_timer, _) in world.get_components(
            CTransform, CShootTimer, CTagEnemy):
        c_shoot_timer.timer -= delta_time
        if c_shoot_timer.timer > 0:
            continue

        if not _is_on_screen(c_transform, c_viewport):
            continue

        create_enemy_bullet(world, c_transform.pos, player_pos, lander_cfg)
        c_shoot_timer.reset()


def _get_player_position(world: esper.World):
    for _, (c_transform, _, _) in world.get_components(
            CTransform, CPlayerState, CTagPlayer):
        return c_transform.pos
    return None


def _get_viewport(world: esper.World):
    for _, c_viewport in world.get_component(CViewport):
        return c_viewport
    return None


def _is_on_screen(c_transform: CTransform, c_viewport: CViewport) -> bool:
    screen_x = c_viewport.world_to_screen_x(c_transform.pos.x)
    return 0 <= screen_x <= c_viewport.screen_width
