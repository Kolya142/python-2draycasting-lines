import random

import guiintergration.time
import raycast
import settings
from player.camera import Renderer, RenderTypes, RenderTask, Camera
from player.mini_map import MiniMap
from guiintergration import keyboard
from guiintergration.keyboard import Keys
from guiintergration import sound
from guiintergration import mouse
import utils
from math import sin, cos
from vectors import Vec2, Vec3


class Player:
    def __init__(self, game):
        self.angle_y = None
        self.angle_x = None
        self.z_pos_vel = None
        self.pos = None
        self.game = game
        self.speed = 0.3
        self.rotate_speed = -0.07
        self.renderer = Renderer()
        self.camera = Camera(self)
        self.mini_map = MiniMap(self)
        self.restart()
        self.jump_sound = sound.Sound.load_sound("assets/jump15.wav")
        sound.Sound.set_volume(self.jump_sound, 0.0)
        self.font = self.renderer.load_font("assets/Pixeltype.ttf", 30)
        print(self.jump_sound, self.font)

    def restart(self):
        self.pos = Vec3(settings.start_player_x_pos, settings.start_player_y_pos, 0)
        self.z_pos_vel = 0
        self.angle_x = 0
        self.angle_y = 0

    def update(self):

        _args = Vec2(0, 0), Vec2(settings.window_size, settings.window_size//2+self.angle_y), (0, 0, 255)
        self.renderer.add_render_task(RenderTask(RenderTypes.BOX, _args))
        _args = Vec2(0, settings.window_size//2+self.angle_y), \
            Vec2(settings.window_size, settings.window_size), (150, 150, 150)
        self.renderer.add_render_task(RenderTask(RenderTypes.BOX, _args))
        r = self.camera.render()
        # for obj in self.test_world:
        #     self.renderer.add_render_task(RenderTask(RenderTypes.LINE, (obj.a, obj.b, obj.color)))
        #
        # self.renderer.add_render_task(RenderTask(RenderTypes.CIRCLE, (self.pos, 5, (255, 0, 0))))
        # self.renderer.add_render_task(RenderTask(RenderTypes.LINE,
        #     (self.pos, utils.cast_line(self.pos.x, self.pos.y, self.angle_x, 50), (0, 100, 100))))
        self.mini_map.update(r)
        self.renderer.add_render_task(
            RenderTask(RenderTypes.TEXT, (f'fps: {round(guiintergration.time.get_fps(), 2)}', (0, 0), self.font, (0, 255, 0)))
            # text: str, pos: Vec2, font: int, color: Tuple[int, int, int]
        )
        self.renderer.update()
        run_multiplier = 1
        if keyboard.get_pressed(Keys.KEY_LSHIFT):
            run_multiplier = 2
        if keyboard.get_pressed(Keys.KEY_W):
            pos = Vec2()
            pos.x = self.pos.x + sin(self.angle_x) * self.speed * run_multiplier
            pos.y = self.pos.y + cos(self.angle_x) * self.speed * run_multiplier
            # sound.Sound.play_sound(self.walk_sound)
            if settings.collision:
                if raycast.ray_cast_vector(self.pos.x, self.pos.y, pos.x, pos.y, self.game.world) > self.speed*10:
                    self.pos.x += sin(self.angle_x) * self.speed * run_multiplier
                    self.pos.y += cos(self.angle_x) * self.speed * run_multiplier
            else:
                self.pos.x += sin(self.angle_x) * self.speed * run_multiplier
                self.pos.y += cos(self.angle_x) * self.speed * run_multiplier
        if keyboard.get_pressed(Keys.KEY_A):
            self.pos.y -= sin(self.angle_x) * self.speed * run_multiplier
            self.pos.x += cos(self.angle_x) * self.speed * run_multiplier
        if keyboard.get_pressed(Keys.KEY_S):
            self.pos.x -= sin(self.angle_x) * self.speed * run_multiplier
            self.pos.y -= cos(self.angle_x) * self.speed * run_multiplier
        if keyboard.get_pressed(Keys.KEY_D):
            self.pos.y += sin(self.angle_x) * self.speed * run_multiplier
            self.pos.x -= cos(self.angle_x) * self.speed * run_multiplier

        if keyboard.get_pressed(Keys.KEY_LEFT) or mouse.get_position()[0] < settings.window_size//2:
            self.angle_x -= self.rotate_speed
        if keyboard.get_pressed(Keys.KEY_RIGHT) or mouse.get_position()[0] > settings.window_size//2:
            self.angle_x += self.rotate_speed
        if settings.vertical_rotating:
            if keyboard.get_pressed(Keys.KEY_UP) or mouse.get_position()[1] < settings.window_size//2:
                self.angle_y -= self.rotate_speed*200
            if keyboard.get_pressed(Keys.KEY_DOWN) or mouse.get_position()[1] > settings.window_size//2:
                self.angle_y += self.rotate_speed*200
        if keyboard.get_pressed(Keys.KEY_ESC):
            quit()
        if keyboard.get_pressed(Keys.KEY_SPACE) and self.pos.z <= 2:
            self.z_pos_vel += settings.jump_force
            sound.Sound.play_sound(self.jump_sound)
        if keyboard.get_pressed(Keys.KEY_R):
            self.restart()
        if settings.no_clip:
            if keyboard.get_pressed(Keys.KEY_Q):
                self.pos.z -= self.speed * run_multiplier * 200

            if keyboard.get_pressed(Keys.KEY_E):
                self.pos.z += self.speed * run_multiplier * 200
        self.angle_y = utils.clamp(self.angle_y, -480, 480)
        mouse.set_position((settings.window_size//2, settings.window_size//2))
        # gravity
        if not settings.no_clip:
            self.z_pos_vel += settings.gravity
            self.pos.z += self.z_pos_vel
            self.pos.z = max(0, self.pos.z)
