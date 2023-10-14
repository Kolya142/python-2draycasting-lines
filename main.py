from typing import List

from guiintergration import mouse, time

import settings
from obj import Obj
from player.player_class import Player


class Game:
    def __init__(self):
        self.player = Player(self)
        self.world: List[Obj] = []
        if settings.mouse_hide:
            mouse.set_visible(0)

    def main_loop(self):
        while True:
            self.player.update()
            time.set_fps(60)


if __name__ == '__main__':
    game = Game()
    game.main_loop()
