import dataclasses
from typing import List, Dict

import utils
from obj import Obj


@dataclasses.dataclass
class RayCastResult:
    x_pos: float
    y_pos: float
    dist: float
    obj: Obj | None
    hit: bool


def ray_cast(x_pos, y_pos, a, max_length: int, world: List[Obj]) -> List[RayCastResult]:
    cast = utils.cast_line(x_pos, y_pos, a, max_length)
    line = (x_pos, y_pos, cast[0], cast[1])
    dists: Dict[float, Obj] = {}
    for obj in world:
        pos = utils.find_intersection(line, (*obj.a, *obj.b))
        # pos = line[2], line[3]
        if not pos:
            continue
        x, y = pos
        dists[utils.distance_between_points(x, y, x_pos, y_pos)] = obj

    if dists == {}:
        return [RayCastResult(line[2], line[3], max_length, None, False)]

    p = sorted(list(dists.keys()))
    result = []
    for m in p:
        obj = dists[m]
        x, y = utils.find_intersection(line, (*obj.a, *obj.b))
        # x, y = cast
        result.append(RayCastResult(x, y, m, obj, True))
    return result


def ray_cast_vector(x_pos, y_pos, x_end_pos, y_end_pos, world: List[Obj]) -> float:
    line = (x_pos, y_pos, x_end_pos, y_end_pos)
    dists: Dict[float, Obj] = {}
    for obj in world:
        pos = utils.find_intersection(line, (*obj.a, *obj.b))
        # pos = line[2], line[3]
        if not pos:
            continue
        x, y = pos
        dists[utils.distance_between_points(x, y, x_pos, y_pos)] = obj

    if dists == {}:
        return utils.distance_between_points(x_pos, y_pos, x_end_pos, y_end_pos)

    p = sorted(list(dists.keys()))
    result = []
    for m in p:
        obj = dists[m]
        x, y = utils.find_intersection(line, (*obj.a, *obj.b))
        # x, y = cast
        result.append(RayCastResult(x, y, m, obj, True))
    return result[0].dist

