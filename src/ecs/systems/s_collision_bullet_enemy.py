import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_enemy_lander_state import CEnemyLanderState, LanderState
from src.ecs.components.c_humanoid_state import CHumanoidState, HumanoidState
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
                _on_enemy_destroyed(world, enemy_entity, e_transform)
                if world.entity_exists(bullet_entity):
                    world.delete_entity(bullet_entity)
                break


def _on_enemy_destroyed(world: esper.World, enemy_entity: int,
                        e_transform: CTransform):
    _rescue_humanoid_if_captured(world, enemy_entity)
    create_enemy_explosion(world, e_transform.pos.copy())
    ServiceLocator.sounds_service.play("assets/snd/enemy_die.ogg")
    world.delete_entity(enemy_entity)


def _rescue_humanoid_if_captured(world: esper.World, enemy_entity: int):
    if not world.has_component(enemy_entity, CEnemyLanderState):
        return

    c_lander_state = world.component_for_entity(enemy_entity, CEnemyLanderState)
    if c_lander_state.state != LanderState.CAPTURE:
        return
    if c_lander_state.target_humanoid == -1:
        return
    if not world.entity_exists(c_lander_state.target_humanoid):
        return

    humanoid_state = world.component_for_entity(
        c_lander_state.target_humanoid, CHumanoidState)
    humanoid_state.state = HumanoidState.ON_GROUND
    ServiceLocator.sounds_service.play("assets/snd/astronaut_fall.ogg")
