from typing import List

from guiintergration import mouse, keyboard
import settings
from obj import Obj
from player.camera import Renderer, RenderTask, RenderTypes

if __name__ == '__main__':
    display = Renderer()
    world: List[Obj] = []
    is_edit = False
    # FIXME
    while True:
        for obj in world:
            a = list(obj.a)
            b = list(obj.b)
            a[0] = a[0] / settings.world_size * settings.window_size
            a[1] = a[1] / settings.world_size * settings.window_size
            b[0] = b[0] / settings.world_size * settings.window_size
            b[1] = b[1] / settings.world_size * settings.window_size
            task = RenderTask(RenderTypes.LINE, (a, b, (0, 0, 0)))
            display.add_render_task(task)
        display.update()

