import dataclasses
import enum
from typing import List
from math import cos

import raycast
import settings
from guiintergration.screen import Screen


class RenderTypes(enum.Enum):
    CIRCLE = 0
    LINE = 1
    BOX = 2


@dataclasses.dataclass
class RenderTask:
    type_: RenderTypes
    args_: tuple


class Renderer:
    def __init__(self):
        self._screen = Screen((settings.window_size, settings.window_size))
        self._render_buffer: List[RenderTask] = []

    def add_render_task(self, task: RenderTask):
        self._render_buffer.append(task)

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
        self._screen.update()


class Camera:
    def __init__(self, player):
        self.player = player

    def render(self):
        angle = self.player.angle_x + settings.rays_count//2 * settings.ray_step_angle
        x = 0
        x_step = settings.window_size / settings.rays_count
        for _ in range(settings.rays_count):
            angle -= settings.ray_step_angle
            traces = raycast.ray_cast(self.player.pos[0], self.player.pos[1],
                                     angle, 400, self.player.game.world)
            for trace in traces:
                npos = (trace.x_pos, trace.y_pos)
                if trace.hit:
                    b = 100
                    d = trace.dist
                    # fish eye fix FIXME
                    if settings.fish_eye_fix and False:
                        d /= cos(angle)
                    # d_shr = trace.obj.z_size
                    # formula from http://ilinblog.ru/article.php?id_article=49
                    d_shr = 50
                    b_shr = d_shr / d * b
                    ds = d / 20
                    color = list(trace.obj.color)
                    color[0] *= 1/ds
                    color[1] *= 1/ds
                    color[2] *= 1/ds
                    color[0] = max(0, min(color[0], 200))
                    color[1] = max(0, min(color[1], 200))
                    color[2] = max(0, min(color[2], 200))
                    self.player.renderer.add_render_task(RenderTask(RenderTypes.BOX,
                                                                    ((x, settings.window_size//2 - b_shr+self.player.angle_y-(50-d_shr)),
                                                                     (round(x_step), b_shr*2), color)))

                    # DEBUG DRAW
                    npos_1 = [npos[0]-self.player.pos[0]+100, npos[1]-self.player.pos[1]+100]
                    npos_1[0] = max(min(npos_1[0], 200), 0)
                    npos_1[1] = max(min(npos_1[1], 200), 0)
                    self.player.renderer.add_render_task(
                        RenderTask(RenderTypes.LINE, ((100, 100), npos_1, (200, 250, 200))))
                    self.player.renderer.add_render_task(
                        RenderTask(RenderTypes.CIRCLE, (npos_1, 2, trace.obj.color)))
                break
            x += x_step
