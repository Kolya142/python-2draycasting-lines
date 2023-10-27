import dataclasses
from typing import Tuple

from guiintergration.texture import Texture
from vectors import Vec2


@dataclasses.dataclass
class Obj:
    a: Vec2
    b: Vec2
    color: Tuple[int, int, int] = None
    z_pos: int = 0
    texture: Texture = None
