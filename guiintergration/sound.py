from typing import Dict

import pygame

pygame.mixer.init()


class Sound:
    __instance_: Dict[int, pygame.mixer.Sound] = {}

    @classmethod
    def load_sound(cls, filename: str) -> int:
        n = hash(filename)
        cls.__instance_[n] = pygame.mixer.Sound(filename)
        return n

    @classmethod
    def set_volume(cls, address: int, volume: float):
        cls.__instance_[address].set_volume(volume)

    @classmethod
    def stop_sound(cls, address: int):
        cls.__instance_[address].stop()

    @classmethod
    def play_sound(cls, address: int):
        cls.__instance_[address].play()
