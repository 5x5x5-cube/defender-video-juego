import esper

from src.ecs.components.c_humanoid_state import CHumanoidState, HumanoidState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_humanoid import CTagHumanoid
from src.create.prefab_creator import create_humanoid_explosion


def system_collision_bullet_humanoid(world: esper.World):
    bullets = list(world.get_components(CTransform, CSurface, CTagBullet))
    humanoids = list(world.get_components(CTransform, CSurface, CHumanoidState, CTagHumanoid))

    humanoids_to_kill = set()

    for _, (b_transform, b_surface, _) in bullets:
        bullet_rect = b_surface.get_area_relative(b_transform.pos)

        for humanoid_entity, (h_transform, h_surface, h_state, _) in humanoids:
            if humanoid_entity in humanoids_to_kill:
                continue
            if h_state.state == HumanoidState.CAPTURED:
                humanoid_rect = h_surface.get_area_relative(h_transform.pos)
                if bullet_rect.colliderect(humanoid_rect):
                    humanoids_to_kill.add(humanoid_entity)

    for humanoid_entity in humanoids_to_kill:
        if world.entity_exists(humanoid_entity):
            h_transform = world.component_for_entity(humanoid_entity, CTransform)
            create_humanoid_explosion(world, h_transform.pos.copy())
            world.delete_entity(humanoid_entity)
