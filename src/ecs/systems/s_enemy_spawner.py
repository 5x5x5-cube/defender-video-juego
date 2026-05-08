import random

import esper

from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.load.load_world import LanderConfig
from src.create.prefab_creator import create_enemy_lander


def system_enemy_spawner(world: esper.World, game_time: float,
                         last_spawn_time: float, world_width: float,
                         lander_cfg: LanderConfig) -> float:
    if game_time - last_spawn_time < lander_cfg["spawn_interval"]:
        return last_spawn_time

    current_count = len(world.get_component(CTagEnemy))
    if current_count >= lander_cfg["max_count"]:
        return last_spawn_time

    world_x = random.uniform(0, world_width)
    create_enemy_lander(world, world_x, lander_cfg)
    return game_time
