import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_bullet import CTagEnemyBullet
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.create.prefab_creator import create_ship_explosion, create_enemy_explosion
from src.engine.service_locator import ServiceLocator
import src.engine.game_state as game_state


def system_collision_player(world: esper.World):
    if game_state.player_hit:
        return

    player_data = _get_player_data(world)
    if player_data is None:
        return

    player_entity, player_rect = player_data

    _check_enemy_bullet_collision(world, player_entity, player_rect)
    if game_state.player_hit:
        return
    _check_enemy_collision(world, player_entity, player_rect)


def _get_player_data(world: esper.World):
    for player_entity, (c_transform, c_surface, _) in world.get_components(
            CTransform, CSurface, CTagPlayer):
        player_rect = c_surface.get_area_relative(c_transform.pos)
        return player_entity, player_rect
    return None


def _check_enemy_bullet_collision(world: esper.World, player_entity: int,
                                  player_rect):
    for bullet_entity, (c_transform, c_surface, _) in world.get_components(
            CTransform, CSurface, CTagEnemyBullet):
        bullet_rect = c_surface.get_area_relative(c_transform.pos)
        if player_rect.colliderect(bullet_rect):
            world.delete_entity(bullet_entity)
            _player_hit(world, player_entity, player_rect)
            return


def _check_enemy_collision(world: esper.World, player_entity: int,
                           player_rect):
    for enemy_entity, (c_transform, c_surface, _) in world.get_components(
            CTransform, CSurface, CTagEnemy):
        enemy_rect = c_surface.get_area_relative(c_transform.pos)
        if player_rect.colliderect(enemy_rect):
            create_enemy_explosion(world, c_transform.pos.copy())
            world.delete_entity(enemy_entity)
            _player_hit(world, player_entity, player_rect)
            return


def _player_hit(world: esper.World, player_entity: int, player_rect):
    center = player_rect.center
    create_ship_explosion(world, pygame.Vector2(center[0], center[1]))
    ServiceLocator.sounds_service.play("assets/snd/player_die.ogg")
    world.delete_entity(player_entity)
    game_state.player_hit = True
