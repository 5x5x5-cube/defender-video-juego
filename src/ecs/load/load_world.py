import pygame
import json
from typing import TypedDict


class WindowConfig(TypedDict):
    title: str
    size: pygame.Vector2
    bg_color: pygame.Color
    framerate: int


def load_window_config(file_path: str) -> WindowConfig:
    with open(file_path, 'r') as file:
        data = json.load(file)

    return {
        "title": data["title"],
        "size": pygame.Vector2(data["size"]["w"], data["size"]["h"]),
        "bg_color": pygame.Color(data["bg_color"]["r"], data["bg_color"]["g"], data["bg_color"]["b"]),
        "framerate": data["framerate"]
    }
