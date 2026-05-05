import pygame


class CStarBlink:
    def __init__(self, rate: float, color: pygame.Color) -> None:
        self.rate = rate
        self.color = color
        self.timer = 0.0
        self.visible = True
