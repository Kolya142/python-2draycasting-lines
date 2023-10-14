import pygame.time
clock = pygame.time.Clock()


def set_fps(fps: float):
    clock.tick(fps)


def get_fps() -> float:
    return clock.get_fps()


def get_time() -> float:
    return clock.get_time()
