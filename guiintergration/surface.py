import pygame

from utils import clamp
from vectors import Vec2, vec2tuple

Surf = pygame.Surface


def resize(surf: Surf, size: Vec2) -> Surf:
    return pygame.transform.scale(surf, vec2tuple(size))


def mult(surf: Surf, brightness: int):
    brightness = clamp(brightness, 0, 255)
    surf.fill((brightness, brightness, brightness), special_flags=pygame.BLEND_RGBA_MULT)
