from typing import List

import raycast
import settings
from player.camera import Renderer, RenderTypes, RenderTask
from utils import clamp
from obj import Obj
from vectors import Vec2


class MiniMap:
    def __init__(self, player):
        self.player = player

    def update(self, r: List[raycast.RayCastResult]):
        offset = 1 / settings.world_size * settings.mini_map_size
        player_pos = Vec2(self.player.pos.x, self.player.pos.y) * offset
        player_pos.x += settings.window_size-settings.mini_map_size
        a = Vec2(settings.window_size-settings.mini_map_size, 0)
        b = Vec2(settings.mini_map_size, settings.mini_map_size)

        self.player.renderer.add_render_task(RenderTask(RenderTypes.BOX, (a, b, (255, 255, 255))))
        self.player.renderer.add_render_task(RenderTask(RenderTypes.CIRCLE, (player_pos, 5, (255, 0, 0))))
        for result in r:
            p = Vec2(result.x_pos, result.y_pos) * offset
            p.x += settings.window_size - settings.mini_map_size
            self.player.renderer.add_render_task(RenderTask(RenderTypes.LINE, (player_pos, p, (55, 200, 55))))

        for obj in self.player.game.world:
            a = obj.a.copy() * offset
            b = obj.b.copy() * offset
            a.x += settings.window_size - settings.mini_map_size
            b.x += settings.window_size - settings.mini_map_size
            self.player.renderer.add_render_task(RenderTask(RenderTypes.LINE, (a, b, obj.color)))
