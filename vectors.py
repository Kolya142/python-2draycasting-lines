class Vec2:
    x: float
    y: float

    def __init__(self, x=None, y=None):
        self.x = x
        if x is None:
            x = 0
            self.x = 0
        if y is None:
            self.y = x
        else:
            self.y = y

    def __sub__(self, other):
        if isinstance(other, int):
            self.x -= other
            self.y -= other
        if isinstance(other, Vec2):
            self.x -= other.x
            self.y -= other.y
        return self

    def __add__(self, other):
        if isinstance(other, int):
            self.x += other
            self.y += other
        if isinstance(other, Vec2):
            self.x += other.x
            self.y += other.y
        return self

    def __truediv__(self, other):
        if isinstance(other, int):
            self.x /= other
            self.y /= other
        if isinstance(other, Vec2):
            self.x /= other.x
            self.y /= other.y
        return self

    def __floordiv__(self, other):
        if isinstance(other, int):
            self.x //= other
            self.y //= other
        if isinstance(other, Vec2):
            self.x //= other.x
            self.y //= other.y
        return self

    def __mul__(self, other):
        if isinstance(other, int):
            self.x *= other
            self.y *= other
        if isinstance(other, Vec2):
            self.x *= other.x
            self.y *= other.y
        return self

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def copy(self):
        return Vec2(self.x, self.y)


class Vec3:
    x: float
    y: float
    z: float

    def __init__(self, x=None, y=None, z=None):
        self.x = x
        if x is None:
            x = 0
            self.x = 0
        if y is not None and z is None:
            raise
        if z is None and y is None:
            self.y = x
            self.z = x
        else:
            self.y = y
            self.z = z

    def __sub__(self, other):
        if isinstance(other, int):
            self.x -= other
            self.y -= other
            self.z -= other
        if isinstance(other, Vec3):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.z
        return self

    def __add__(self, other):
        if isinstance(other, int):
            self.x += other
            self.y += other
            self.z += other
        if isinstance(other, Vec3):
            self.x += other.x
            self.y += other.y
            self.z += other.y
        return self

    def __truediv__(self, other):
        if isinstance(other, int):
            self.x -= other
            self.y -= other
            self.z -= other
        if isinstance(other, Vec3):
            self.x -= other.x
            self.y -= other.y
            self.z -= other.y
        return self

    def __mul__(self, other):
        if isinstance(other, int):
            self.x *= other
            self.y *= other
            self.z *= other
        if isinstance(other, Vec3):
            self.x *= other.x
            self.y *= other.y
            self.z *= other.y
        return self


def vec2tuple(vec) -> tuple:
    if isinstance(vec, Vec2):
        return vec.x, vec.y
    if isinstance(vec, Vec3):
        return vec.x, vec.y, vec.z
    if isinstance(vec, tuple):
        return vec
    raise ValueError(f'cannot convert type ({type(vec)}) to tuple')

