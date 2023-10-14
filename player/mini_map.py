import settings
from player.camera import Renderer, RenderTypes, RenderTask
from utils import clamp
from obj import Obj


class MiniMap:
    def __init__(self, player):
        self.player = player

    def update(self):
        offset = 1 / settings.world_size * settings.mini_map_size
        player_pos = self.player.pos.copy()
        player_pos[0] *= offset
        player_pos[1] *= offset
        player_pos[0] += settings.window_size-settings.mini_map_size
        a = (settings.window_size-settings.mini_map_size, 0)
        b = (settings.mini_map_size, settings.mini_map_size)

        self.player.renderer.add_render_task(RenderTask(RenderTypes.BOX, (a, b, (255, 255, 255))))
        self.player.renderer.add_render_task(RenderTask(RenderTypes.CIRCLE, (player_pos, 5, (255, 0, 0))))
        for obj in self.player.game.world:
            a = list(obj.a)
            b = list(obj.b)
            a[0] *= offset
            a[1] *= offset
            b[0] *= offset
            b[1] *= offset
            a[0] += settings.window_size - settings.mini_map_size
            b[0] += settings.window_size - settings.mini_map_size
            self.player.renderer.add_render_task(RenderTask(RenderTypes.LINE, (a, b, obj.color)))
