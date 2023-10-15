from typing import Tuple, Dict

import pygame

from vectors import Vec2, vec2tuple

pygame.font.init()


class Screen:
    _core_screen: pygame.Surface
    _fonts: Dict[int, pygame.font.Font] = {}

    def __init__(self, size: Vec2):
        self._core_screen = pygame.display.set_mode(vec2tuple(size))

    def load_font(self, name: str, size: int) -> int:
        hash_ = hash((name, size))
        self._fonts[hash_] = pygame.font.Font(name, size)
        return hash_

    def fill(self, color: Tuple[int, int, int]):
        self._core_screen.fill(color)

    def draw_circle(self, pos: Vec2, radius: int, color: Vec2):
        pygame.draw.circle(self._core_screen, vec2tuple(color), vec2tuple(pos), radius)

    def draw_line(self, a: Vec2, b: Vec2, color: Tuple[int, int, int]):
        pygame.draw.line(self._core_screen, color, vec2tuple(a), vec2tuple(b))

    def draw_box(self, a: Vec2, b: Vec2, color: Tuple[int, int, int]):
        pygame.draw.rect(self._core_screen, color, (vec2tuple(a), vec2tuple(b)))

    def draw_text(self, text: str, pos: Vec2, font: int, color: Tuple[int, int, int]):
        surf = self._fonts[font].render(text, False, color)
        self._core_screen.blit(surf, vec2tuple(pos))

    @staticmethod
    def update():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        pygame.display.flip()
