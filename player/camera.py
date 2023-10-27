import dataclasses
import enum
import math
from typing import List
from math import cos
from multiprocessing import Pool

import raycast
import settings
from guiintergration import surface
from guiintergration.screen import Screen
from guiintergration.texture import Texture
from line import Line
from vectors import Vec2


class RenderTypes(enum.Enum):
    CIRCLE = 0
    LINE = 1
    BOX = 2
    TEXT = 3
    TEXTURE = 4


@dataclasses.dataclass
class RenderTask:
    type_: RenderTypes
    args_: tuple


class Renderer:
    def __init__(self):
        self._screen = Screen(Vec2(settings.window_size, settings.window_size))
        self._render_buffer: List[RenderTask] = []

    def add_render_task(self, task: RenderTask):
        self._render_buffer.append(task)

    def load_font(self, name: str, size: int) -> int:
        return self._screen.load_font(name, size)

    def update(self):
        self._screen.fill((0, 0, 0))
        self._render_buffer = self._render_buffer[::-1]
        while self._render_buffer:
            rt = self._render_buffer.pop()
            match rt.type_:
                case RenderTypes.LINE:
                    self._screen.draw_line(*rt.args_)
                case RenderTypes.BOX:
                    self._screen.draw_box(*rt.args_)
                case RenderTypes.CIRCLE:
                    self._screen.draw_circle(*rt.args_)
                case RenderTypes.TEXT:
                    self._screen.draw_text(*rt.args_)
                case RenderTypes.TEXTURE:
                    self._screen.blit(*rt.args_)
        self._screen.update()


def for_render(trace, angle, self, x, x_step, texture: Texture):
    npos = Vec2(trace.x_pos, trace.y_pos)
    if trace.hit:
        b = 100
        d = trace.dist
        d = max(0.0001, d)
        # fish eye fix FIXME
        if settings.fish_eye_fix:
            d *= cos(angle - self.player.angle_x)
        # d_shr = trace.obj.z_size
        # formula from http://ilinblog.ru/article.php?id_article=49
        d_shr = 50
        b_shr = d_shr / d * b
        ds = d / 20
        angle_y = self.player.angle_y + self.player.pos.z / d  # - 3 * d
        if settings.window_size // 2 - b_shr + angle_y - (50 - d_shr) > settings.window_size:
            return
        color = list(trace.obj.color)
        color[0] *= 1 / ds
        color[1] *= 1 / ds
        color[2] *= 1 / ds
        color[0] = max(0, min(color[0], 200))
        color[1] = max(0, min(color[1], 200))
        color[2] = max(0, min(color[2], 200))
        if not settings.texturing:
            self.player.renderer.add_render_task(RenderTask(RenderTypes.BOX,
                                                            (
                                                                Vec2(x, settings.window_size // 2 - b_shr + angle_y - (
                                                                        50 - d_shr)),
                                                                Vec2(round(x_step), b_shr * 2), color)))
        else:
            tx = trace.x_pos % settings.map_scale.x
            ty = trace.y_pos % settings.map_scale.y
            h = texture.get_size().y
            w = texture.get_size().x
            kkk = round(w / settings.FOV)
            side = 0
            if ty == 0:
                side = 1
            offset = tx/settings.map_scale.x if side else ty/settings.map_scale.y
            offset = min(int(w*offset), int(w - 3))
            s = Vec2(offset, 0)
            e = Vec2(kkk, h)
            e.x = min(e.x, w-s.x)
            print(s.x, s.y, e.x, e.y)
            sur = texture.get_sub_surface(s, e)
            sur = surface.resize(sur, Vec2(round(x_step), b_shr * 2))
            surface.mult(sur, int(1 / ds * 255))
            self.player.renderer.add_render_task(RenderTask(RenderTypes.TEXTURE,
                                                            (
                                                                sur,
                                                                Vec2(x, settings.window_size // 2 - b_shr + angle_y - (
                                                                        50 - d_shr)),
                                                            )))
            del sur

        # DEBUG DRAW
        # npos_1 = Vec2(npos[0] - self.player.pos[0] + 100, npos[1] - self.player.pos[1] + 100)
        npos_1 = npos - Vec2(self.player.pos.x, self.player.pos.y) + 100
        npos_1.x = max(min(npos_1.x, 200), 0)
        npos_1.y = max(min(npos_1.y, 200), 0)
        self.player.renderer.add_render_task(
            RenderTask(RenderTypes.LINE, (Vec2(100, 100), npos_1, (200, 250, 200))))
        self.player.renderer.add_render_task(
            RenderTask(RenderTypes.CIRCLE, (npos_1, 2, trace.obj.color)))


class Camera:
    def __init__(self, player):
        self.player = player

    def render(self) -> List[raycast.RayCastResult]:
        angle = self.player.angle_x + settings.FOV // 2 * settings.ray_step_angle
        x = 0
        x_step = settings.window_size / settings.FOV
        results = []
        for _ in range(settings.FOV):
            angle -= settings.ray_step_angle
            traces = raycast.ray_cast(self.player.pos.x, self.player.pos.y,
                                      angle, 400, self.player.game.world)[::-1]
            results.append(traces[-1])
            if self.player.pos.z > 200 or 1:
                for trace in traces:
                    if trace.obj is not None:
                        for_render(trace, angle, self, x, x_step, trace.obj.texture)
                        continue
                    for_render(trace, angle, self, x, x_step, None)
            else:
                for_render(traces[-1], angle, self, x, x_step, traces[-1].obj.texture)
            x += x_step
        return results
