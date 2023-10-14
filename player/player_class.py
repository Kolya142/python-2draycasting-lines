import random

import raycast
import settings
from player.camera import Renderer, RenderTypes, RenderTask, Camera
from player.mini_map import MiniMap
from guiintergration import keyboard
from guiintergration.keyboard import Keys
from guiintergration import mouse
import utils
from math import sin, cos
from obj import Obj


class Player:
    def __init__(self, game):
        self.game = game
        self.pos = [settings.start_player_x_pos, settings.start_player_y_pos]
        self.angle_x = 0
        self.angle_y = 0
        self.speed = 0.1
        self.rotate_speed = -0.05
        self.renderer = Renderer()
        self.camera = Camera(self)
        self.mini_map = MiniMap(self)
        self.restart()

    def restart(self):
        self.game.world = [Obj(
            (random.randint(0, 500), random.randint(0, 500)),
            (random.randint(0, 500), random.randint(0, 500)),
            utils.random_color_8bit_tuple(), random.randint(20, 50)) for _ in range(50)]
        self.pos = [settings.start_player_x_pos, settings.start_player_y_pos]
        self.angle_x = 0
        self.angle_y = 0

    def update(self):

        _args = (0, 0), (settings.window_size, settings.window_size//2+self.angle_y), (0, 0, 255)
        self.renderer.add_render_task(RenderTask(RenderTypes.BOX, _args))
        _args = (0, settings.window_size//2+self.angle_y), \
            (settings.window_size, settings.window_size), (150, 150, 150)
        self.renderer.add_render_task(RenderTask(RenderTypes.BOX, _args))
        self.camera.render()
        # for obj in self.test_world:
        #     self.renderer.add_render_task(RenderTask(RenderTypes.LINE, (obj.a, obj.b, obj.color)))
        #
        # self.renderer.add_render_task(RenderTask(RenderTypes.CIRCLE, (self.pos, 5, (255, 0, 0))))
        # self.renderer.add_render_task(RenderTask(RenderTypes.LINE,
        #     (self.pos, utils.cast_line(self.pos[0], self.pos[1], self.angle_x, 50), (0, 100, 100))))
        self.mini_map.update()
        self.renderer.update()
        run_multiplier = 1
        if keyboard.get_pressed(Keys.KEY_LSHIFT):
            run_multiplier = 2
        if keyboard.get_pressed(Keys.KEY_W):
            self.pos[0] += sin(self.angle_x) * self.speed * run_multiplier
            self.pos[1] += cos(self.angle_x) * self.speed * run_multiplier
        if keyboard.get_pressed(Keys.KEY_A):
            self.pos[1] -= sin(self.angle_x) * self.speed * run_multiplier
            self.pos[0] += cos(self.angle_x) * self.speed * run_multiplier
        if keyboard.get_pressed(Keys.KEY_S):
            self.pos[0] -= sin(self.angle_x) * self.speed * run_multiplier
            self.pos[1] -= cos(self.angle_x) * self.speed * run_multiplier
        if keyboard.get_pressed(Keys.KEY_D):
            self.pos[1] += sin(self.angle_x) * self.speed * run_multiplier
            self.pos[0] -= cos(self.angle_x) * self.speed * run_multiplier

        if keyboard.get_pressed(Keys.KEY_LEFT) or mouse.get_position()[0] < settings.window_size//2:
            self.angle_x -= self.rotate_speed
        if keyboard.get_pressed(Keys.KEY_RIGHT) or mouse.get_position()[0] > settings.window_size//2:
            self.angle_x += self.rotate_speed

        if keyboard.get_pressed(Keys.KEY_UP) or mouse.get_position()[1] < settings.window_size//2:
            self.angle_y -= self.rotate_speed*200
        if keyboard.get_pressed(Keys.KEY_DOWN) or mouse.get_position()[1] > settings.window_size//2:
            self.angle_y += self.rotate_speed*200
        if keyboard.get_pressed(Keys.KEY_ESC):
            quit()
        if keyboard.get_pressed(Keys.KEY_R):
            self.restart()
        self.angle_y = utils.clamp(self.angle_y, -480, 480)
        mouse.set_position((settings.window_size//2, settings.window_size//2))
