import dataclasses
from typing import Tuple


@dataclasses.dataclass
class Obj:
    a: Tuple[int, int]
    b: Tuple[int, int]
    color: Tuple[int, int, int]
    z_size: int
