import pygame
import json
from typing import TypedDict


class WindowConfig(TypedDict):
    title: str
    size: pygame.Vector2
    bg_color: pygame.Color
    framerate: int


class BlinkRateConfig(TypedDict):
    min: float
    max: float


class WorldConfig(TypedDict):
    star_colors: list[pygame.Color]
    stars_number: int
    stars_parallax_factor: float
    stars_blink_rate: BlinkRateConfig
    planet_terrain_colors: list[pygame.Color]
    planet_terrain_line_points: int
    planet_parallax_factor: float
    world_width: int
    camera_lerp_speed: float
    camera_transition_lerp_speed: float
    camera_transition_delay: float


class HumanoidConfig(TypedDict):
    count: int
    wander_speed: float
    wander_range: float
    direction_change_chance: float


class BulletConfig(TypedDict):
    speed: float
    max_count: int
    width: int
    height: int


class BurnerAnimConfig(TypedDict):
    image: str
    number_frames: int
    list: list[dict]


class PlayerConfig(TypedDict):
    image: str
    acceleration: float
    deceleration: float
    reverse_deceleration: float
    max_speed: float
    vertical_speed: float
    initial_position: pygame.Vector2
    animations: dict


class InterfaceConfig(TypedDict):
    title_text_color: pygame.Color
    normal_text_color: pygame.Color
    high_score_color: pygame.Color
    high_score_max_value: int
    hud_height: int
    hud_line_color: pygame.Color
    radar_width: int
    radar_height: int


def load_window_config(file_path: str) -> WindowConfig:
    with open(file_path, 'r') as file:
        data = json.load(file)

    return {
        "title": data["title"],
        "size": pygame.Vector2(data["size"]["w"], data["size"]["h"]),
        "bg_color": pygame.Color(data["bg_color"]["r"], data["bg_color"]["g"], data["bg_color"]["b"]),
        "framerate": data["framerate"]
    }


def load_world_config(file_path: str) -> WorldConfig:
    with open(file_path, 'r') as file:
        data = json.load(file)

    return {
        "star_colors": [
            pygame.Color(c["r"], c["g"], c["b"]) for c in data["star_colors"]
        ],
        "stars_number": data["stars_number"],
        "stars_parallax_factor": data["stars_parallax_factor"],
        "stars_blink_rate": {
            "min": data["stars_blink_rate"]["min"],
            "max": data["stars_blink_rate"]["max"]
        },
        "planet_terrain_colors": [
            pygame.Color(c["r"], c["g"], c["b"]) for c in data["planet_terrain_colors"]
        ],
        "planet_terrain_line_points": data["planet_terrain_line_points"],
        "planet_parallax_factor": data["planet_parallax_factor"],
        "world_width": data["world_width"],
        "camera_lerp_speed": data["camera_lerp_speed"],
        "camera_transition_lerp_speed": data["camera_transition_lerp_speed"],
        "camera_transition_delay": data["camera_transition_delay"]
    }


def load_player_config(file_path: str) -> PlayerConfig:
    with open(file_path, 'r') as file:
        data = json.load(file)

    return {
        "image": data["image"],
        "acceleration": data["acceleration"],
        "deceleration": data["deceleration"],
        "reverse_deceleration": data["reverse_deceleration"],
        "max_speed": data["max_speed"],
        "vertical_speed": data["vertical_speed"],
        "initial_position": pygame.Vector2(
            data["initial_position"]["x"],
            data["initial_position"]["y"]
        ),
        "animations": data["animations"]
    }


def load_humanoid_config(file_path: str) -> HumanoidConfig:
    with open(file_path, 'r') as file:
        data = json.load(file)

    return {
        "count": data["count"],
        "wander_speed": data["wander_speed"],
        "wander_range": data["wander_range"],
        "direction_change_chance": data["direction_change_chance"]
    }


def load_bullet_config(file_path: str) -> BulletConfig:
    with open(file_path, 'r') as file:
        data = json.load(file)

    return {
        "speed": data["speed"],
        "max_count": data["max_count"],
        "width": data["width"],
        "height": data["height"]
    }


def load_interface_config(file_path: str) -> InterfaceConfig:
    with open(file_path, 'r') as file:
        data = json.load(file)

    return {
        "title_text_color": pygame.Color(
            data["title_text_color"]["r"],
            data["title_text_color"]["g"],
            data["title_text_color"]["b"]
        ),
        "normal_text_color": pygame.Color(
            data["normal_text_color"]["r"],
            data["normal_text_color"]["g"],
            data["normal_text_color"]["b"]
        ),
        "high_score_color": pygame.Color(
            data["high_score_color"]["r"],
            data["high_score_color"]["g"],
            data["high_score_color"]["b"]
        ),
        "high_score_max_value": data["high_score_max_value"],
        "hud_height": data["hud_height"],
        "hud_line_color": pygame.Color(
            data["hud_line_color"]["r"],
            data["hud_line_color"]["g"],
            data["hud_line_color"]["b"]
        ),
        "radar_width": data["radar_width"],
        "radar_height": data["radar_height"]
    }
