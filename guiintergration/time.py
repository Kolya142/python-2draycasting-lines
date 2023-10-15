import pygame.time
clock = pygame.time.Clock()
_fps = 0


def set_max_fps(fps: float):
    global _fps
    _fps = fps


def update():
    clock.tick(_fps)


def get_fps() -> float:
    return clock.get_fps()


def get_time() -> float:
    return clock.get_time()
