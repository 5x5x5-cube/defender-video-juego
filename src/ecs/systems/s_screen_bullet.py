import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet


def system_screen_bullet(world: esper.World):
    c_viewport = _get_viewport(world)
    if c_viewport is None:
        return

    for bullet_entity, (c_transform, _) in world.get_components(CTransform, CTagBullet):
        if _is_outside_viewport(c_transform, c_viewport):
            world.delete_entity(bullet_entity)

    for bullet_entity, (c_transform, _) in world.get_components(CTransform, CTagEnemyBullet):
        if _is_outside_viewport(c_transform, c_viewport):
            world.delete_entity(bullet_entity)


def _get_viewport(world: esper.World):
    for _, c_viewport in world.get_component(CViewport):
        return c_viewport
    return None


def _is_outside_viewport(c_transform: CTransform, c_viewport: CViewport) -> bool:
    screen_x = c_viewport.world_to_screen_x(c_transform.pos.x)
    return screen_x <= 0 or screen_x >= c_viewport.screen_width
