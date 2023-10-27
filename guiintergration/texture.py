import pygame

from typing import Dict, Tuple
from guiintergration.surface import Surf, mult
from line import Line
from utils import clamp
from vectors import Vec2


class Texture:
    _surf: pygame.Surface
    _chahe: Dict[Tuple[Vec2, Vec2], Surf]

    def __init__(self, fn: str):
        self._surf = pygame.image.load(fn)
        self._chahe = {}

    def get_size(self) -> Vec2:
        s = self._surf.get_size()
        return Vec2(s[0], s[1])

    def mult(self, brightness: int):
        mult(self._surf, brightness)

    def get_sub_surface(self, a: Vec2, b: Vec2) -> Surf:
        rect = (a.x, a.y, b.x, b.y)
        rect2 = (a.x//2, a.y//2, b.x//2, b.y//2)
        if rect2 in self._chahe:
            return self._chahe[rect2]
        s = self._surf.subsurface(rect)
        self._chahe[rect2] = s
        return s
