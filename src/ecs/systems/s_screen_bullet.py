import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_screen_bullet(world: esper.World):
    c_viewport = _get_viewport(world)
    if c_viewport is None:
        return

    for bullet_entity, (c_transform, _) in world.get_components(CTransform, CTagBullet):
        screen_x = c_viewport.world_to_screen_x(c_transform.pos.x)
        if _touches_viewport_edge(screen_x, c_viewport.screen_width):
            world.delete_entity(bullet_entity)


def _get_viewport(world: esper.World):
    for _, c_viewport in world.get_component(CViewport):
        return c_viewport
    return None


def _touches_viewport_edge(screen_x: float, screen_width: float) -> bool:
    return screen_x <= 0 or screen_x >= screen_width
