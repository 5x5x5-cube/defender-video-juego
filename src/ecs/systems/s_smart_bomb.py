import esper

from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_viewport import CViewport
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.create.prefab_creator import create_enemy_explosion, create_mutant_explosion
from src.ecs.components.tags.c_tag_mutant import CTagMutant
from src.engine.service_locator import ServiceLocator
import src.engine.game_state as game_state

BOMB_KILL_SCORE = 150


def system_smart_bomb(world: esper.World, screen_width: float):
    if game_state.smart_bombs <= 0:
        return

    c_viewport = _get_viewport(world)
    if c_viewport is None:
        return

    game_state.smart_bombs -= 1
    ServiceLocator.sounds_service.play("assets/snd/enemy_die.ogg")

    enemies_to_kill = []
    for entity, (c_transform, _) in world.get_components(CTransform, CTagEnemy):
        screen_x = c_viewport.world_to_screen_x(c_transform.pos.x)
        if 0 <= screen_x <= screen_width:
            enemies_to_kill.append((entity, c_transform.pos.copy(),
                                    world.has_component(entity, CTagMutant)))

    for entity, pos, is_mutant in enemies_to_kill:
        if not world.entity_exists(entity):
            continue
        world.delete_entity(entity)
        if is_mutant:
            create_mutant_explosion(world, pos)
        else:
            create_enemy_explosion(world, pos)
        game_state.score += BOMB_KILL_SCORE
        game_state.level_kills += 1

    for entity, (c_transform, _) in list(world.get_components(CTransform, CTagEnemyBullet)):
        screen_x = c_viewport.world_to_screen_x(c_transform.pos.x)
        if 0 <= screen_x <= screen_width:
            if world.entity_exists(entity):
                world.delete_entity(entity)


def _get_viewport(world: esper.World):
    for _, c_viewport in world.get_component(CViewport):
        return c_viewport
    return None
