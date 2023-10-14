import pygame.mouse
from typing import Tuple, Union

LEFT_BUTTON = 0
RIGHT_BUTTON = 2
MIDDLE_BUTTON = 1
MOUSE_4_BUTTON = 3
MOUSE_5_BUTTON = 4


def set_visible(value: Union[bool, int]):
    pygame.mouse.set_visible(value)


def set_position(pos: Tuple[int, int]):
    pygame.mouse.set_pos(pos)


def get_position() -> Tuple[int, int]:
    return pygame.mouse.get_pos()


def get_pressed() -> Tuple[int, int, int, int, int]:
    return pygame.mouse.get_pressed(5)

