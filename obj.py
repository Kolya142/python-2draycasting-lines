import dataclasses
from typing import Tuple

from vectors import Vec2


@dataclasses.dataclass
class Obj:
    a: Vec2
    b: Vec2
    color: Tuple[int, int, int]
    z_size: int
