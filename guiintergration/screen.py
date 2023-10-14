from typing import Tuple

import pygame


class Screen:
    _core_screen: pygame.Surface

    def __init__(self, size: Tuple[int, int]):
        self._core_screen = pygame.display.set_mode(size)

    def fill(self, color: Tuple[int, int, int]):
        self._core_screen.fill(color)

    def draw_circle(self, pos: Tuple[int, int], radius: int, color: Tuple[int, int]):
        pygame.draw.circle(self._core_screen, color, pos, radius)

    def draw_line(self, a: Tuple[int, int], b: Tuple[int, int], color: Tuple[int, int, int]):
        pygame.draw.line(self._core_screen, color, a, b)

    def draw_box(self, a: Tuple[int, int], b: Tuple[int, int], color: Tuple[int, int, int]):
        pygame.draw.rect(self._core_screen, color, (a, b))

    @staticmethod
    def update():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
        pygame.display.flip()
