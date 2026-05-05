import esper
import pygame
import pytest

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.systems.s_animation import system_animation


ANIM_LIST = [
    {"name": "walk", "start": 0, "end": 2, "framerate": 10}
]


class TestAnimation:
    def setup_method(self):
        self.world = esper.World()

    def _create_animated_entity(self, num_frames=3, anim_list=None):
        if anim_list is None:
            anim_list = ANIM_LIST
        entity = self.world.create_entity()
        surf = pygame.Surface((num_frames * 10, 10), pygame.SRCALPHA)
        c_surface = CSurface.from_surface(surf)
        c_surface.area = pygame.Rect(0, 0, 10, 10)
        self.world.add_component(entity, c_surface)
        self.world.add_component(entity, CAnimation(num_frames, anim_list))
        return entity

    def test_frame_advances_after_framerate_time(self):
        entity = self._create_animated_entity()
        anim = self.world.component_for_entity(entity, CAnimation)

        assert anim.current_frame == 0

        # framerate=10 means 0.1s per frame
        system_animation(self.world, 0.1)
        assert anim.current_frame == 1

    def test_frame_wraps_to_start(self):
        entity = self._create_animated_entity()
        anim = self.world.component_for_entity(entity, CAnimation)

        system_animation(self.world, 0.1)  # frame 1
        system_animation(self.world, 0.1)  # frame 2
        system_animation(self.world, 0.1)  # wraps to 0

        assert anim.current_frame == 0

    def test_surface_area_updates_with_frame(self):
        entity = self._create_animated_entity()
        surface = self.world.component_for_entity(entity, CSurface)

        assert surface.area.x == 0

        system_animation(self.world, 0.1)
        assert surface.area.x == 10  # second frame

    def test_frame_does_not_advance_before_time(self):
        entity = self._create_animated_entity()
        anim = self.world.component_for_entity(entity, CAnimation)

        # First call always advances (timer starts at 0)
        system_animation(self.world, 0.05)
        assert anim.current_frame == 1

        # Second call within framerate interval should NOT advance
        system_animation(self.world, 0.05)
        assert anim.current_frame == 1


class TestSetAnimation:
    def test_switches_animation_clip(self):
        anim_list = [
            {"name": "idle", "start": 0, "end": 1, "framerate": 10},
            {"name": "run", "start": 2, "end": 4, "framerate": 10}
        ]
        c_anim = CAnimation(5, anim_list)
        assert c_anim.current_frame == 0

        set_animation(c_anim, 1)
        assert c_anim.current_animation == 1
        assert c_anim.current_frame == 2  # start of "run"

    def test_same_animation_does_not_reset(self):
        c_anim = CAnimation(3, ANIM_LIST)
        c_anim.current_frame = 2

        set_animation(c_anim, 0)  # same animation
        assert c_anim.current_frame == 2  # unchanged
