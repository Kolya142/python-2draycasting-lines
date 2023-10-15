from typing import List

from guiintergration import mouse, time

import settings
from obj import Obj
from player.player_class import Player


class Game:
    def __init__(self):
        self.player = Player(self)
        self.world: List[Obj] = settings.world
        if settings.mouse_hide:
            mouse.set_visible(0)

    def main_loop(self):
        time.set_max_fps(60)
        while True:
            self.player.update()
            time.update()


if __name__ == '__main__':
    game = Game()
    game.main_loop()
