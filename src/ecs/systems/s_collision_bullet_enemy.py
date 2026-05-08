import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.create.prefab_creator import create_enemy_explosion
from src.engine.service_locator import ServiceLocator


def system_collision_bullet_enemy(world: esper.World):
    bullets = list(world.get_components(CTransform, CSurface, CTagBullet))
    enemies = list(world.get_components(CTransform, CSurface, CTagEnemy))

    for bullet_entity, (b_transform, b_surface, _) in bullets:
        bullet_rect = b_surface.get_area_relative(b_transform.pos)

        for enemy_entity, (e_transform, e_surface, _) in enemies:
            if not world.entity_exists(enemy_entity):
                continue
            enemy_rect = e_surface.get_area_relative(e_transform.pos)

            if bullet_rect.colliderect(enemy_rect):
                create_enemy_explosion(world, e_transform.pos.copy())
                ServiceLocator.sounds_service.play("assets/snd/enemy_die.ogg")
                world.delete_entity(enemy_entity)
                if world.entity_exists(bullet_entity):
                    world.delete_entity(bullet_entity)
                break
