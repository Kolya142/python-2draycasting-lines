import dataclasses

from vectors import Vec2


@dataclasses.dataclass
class Line:
    a: Vec2
    b: Vec2