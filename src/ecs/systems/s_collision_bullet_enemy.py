import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_mutant import CTagMutant
from src.create.prefab_creator import create_enemy_explosion, create_mutant_explosion
from src.engine.service_locator import ServiceLocator
import src.engine.game_state as game_state

LANDER_SCORE = 150
MUTANT_SCORE = 150


def system_collision_bullet_enemy(world: esper.World):
    bullets = list(world.get_components(CTransform, CSurface, CTagBullet))
    enemies = list(world.get_components(CTransform, CSurface, CTagEnemy))

    enemies_to_kill = set()

    for _, (b_transform, b_surface, _) in bullets:
        bullet_rect = b_surface.get_area_relative(b_transform.pos)

        for enemy_entity, (e_transform, e_surface, _) in enemies:
            if enemy_entity in enemies_to_kill:
                continue
            if not world.entity_exists(enemy_entity):
                continue
            enemy_rect = e_surface.get_area_relative(e_transform.pos)

            if bullet_rect.colliderect(enemy_rect):
                enemies_to_kill.add(enemy_entity)

    for enemy_entity in enemies_to_kill:
        if not world.entity_exists(enemy_entity):
            continue
        e_transform = world.component_for_entity(enemy_entity, CTransform)
        is_mutant = world.has_component(enemy_entity, CTagMutant)
        if is_mutant:
            create_mutant_explosion(world, e_transform.pos.copy())
            game_state.score += MUTANT_SCORE
        else:
            create_enemy_explosion(world, e_transform.pos.copy())
            game_state.score += LANDER_SCORE
        ServiceLocator.sounds_service.play("assets/snd/enemy_die.ogg")
        game_state.level_kills += 1
        world.delete_entity(enemy_entity)
