from random import randint

import utils
from obj import Obj
from vectors import Vec2

window_size = 1000
start_player_x_pos = -10
start_player_y_pos = -10
mouse_hide = True
FOV = 150
jump_force = 1000
vertical_rotating = True
gravity = -10
no_clip = False
world_generated = False
world_size = 600
world = []
if world_generated:
    for _ in range(50):
        a = Vec2(randint(0, world_size), randint(0, world_size))
        b = Vec2(randint(0, world_size), randint(0, world_size))
        color = randint(0, 255), randint(0, 255), randint(0, 255)
        world.append(Obj(
            a,
            b,
            color, randint(20, 50)))
else:
    color_table = {}
    map_ = []

    def add_line(a_, b_, color_):
        world.append(Obj(
            a_,
            b_,
            color_, 50
        ))

    with open("map", 'r') as f:
        for line in f.read().split('\n'):
            if line.startswith('!'):
                ln = line.split(',')
                ln2 = ln[1].split()
                color_table[ln[0][1:]] = tuple(map(int, ln2))
                continue
            if line.startswith(';'):
                continue
            if line.startswith('@'):
                world_size = float(line[1:])
                continue
            if line == '':
                continue
            map_.append(line)

    map_scale = Vec2(world_size / len(map_[0]), world_size / len(map_))
    for row_ in range(len(map_)):
        for col_ in range(len(map_[0])):
            if map_[row_][col_] == 'p':
                start_player_x_pos = col_ * map_scale.x
                start_player_y_pos = row_ * map_scale.y
                continue
            if map_[row_][col_] != '_':
                color = color_table[map_[row_][col_]]
                row = row_ * map_scale.y
                col = col_ * map_scale.x
                a = Vec2(col, row)
                b = Vec2(col+map_scale.x, row)
                add_line(a, b, color)

                a = Vec2(col+map_scale.x, row)
                b = Vec2(col+map_scale.x, row+map_scale.y)
                add_line(a, b, color)

                a = Vec2(col+map_scale.x, row+map_scale.y)
                b = Vec2(col, row+map_scale.y)
                add_line(a, b, color)

                a = Vec2(col, row+map_scale.y)
                b = Vec2(col, row)
                add_line(a, b, color)
    for obj in world:
        for obj1 in world:
            if obj is obj1:
                continue
            d = 3
            if obj.a.x - d <= obj1.a.x <= obj.a.x + d and obj.a.y - d <= obj1.a.y <= obj.a.y + d  \
                    and obj.b.x - d <= obj1.b.x <= obj.b.x + d and obj.b.y - d <= obj1.b.y <= obj.b.y + d:
                if obj in world:
                    world.remove(obj)
                    world.remove(obj1)

mini_map_size = 300
fish_eye_fix = True  # FIXME
collision = False  # FIXME
ray_step_angle = 0.01
