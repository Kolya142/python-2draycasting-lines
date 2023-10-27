from random import randint

import utils
from guiintergration.texture import Texture
from obj import Obj
from vectors import Vec2

window_size = 1000
start_player_x_pos = -10
start_player_y_pos = -10
mouse_hide = False
FOV = 150
jump_force = 500
mouse_bound = False
vertical_rotating = True
gravity = -10
no_clip = True
world_generated = False
texturing = False  # out of memory FIXME
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
            color, randint(0, 20)))
else:
    color_table = {}
    textures = {}
    map_ = []
    code = ''


    def add_line(a_, b_, color_, tex):
        world.append(Obj(
            a_,
            b_,
            color_, 50,
            tex
        ))


    with open("map", 'r') as f:
        for line in f.read().split('\n'):
            if line.startswith('!'):
                if not texturing:
                    ln = line.split(',')
                    ln2 = ln[1].split()
                    color_table[ln[0][1:]] = tuple(map(int, ln2))
                else:
                    ln = line.split(',')
                    textures[ln[0][1:]] = ln[1]
                    print(textures)
                continue
            if line.startswith(';'):
                continue
            if line.startswith('#'):
                ln = line[1:].split('=')
                if ln[0] == "map":
                    world_size = float(ln[1])
                if ln[0] == "tex":
                    texturing = not not int(ln[1])
                continue
            if line.startswith('@'):
                code += line[1:] + '\n'
                continue
            if line == '':
                continue
            map_.append(line)

    map_scale = Vec2(world_size / len(map_[0]), world_size / len(map_))
    # Initialize a set for unique lines
    unique_lines = []

    for row_ in range(len(map_)):
        for col_ in range(len(map_[0])):
            cell = map_[row_][col_]
            if cell == 'p':
                start_player_x_pos = col_ * map_scale.x
                start_player_y_pos = row_ * map_scale.y
                continue
            if cell == '_':
                continue

            if not texturing:
                color = color_table[cell]
                texture = None
            else:
                color = (0, 0, 0)
                texture = Texture(textures[cell])

            row = row_ * map_scale.y
            col = col_ * map_scale.x

            a = Vec2(col, row)
            b = Vec2(col + map_scale.x, row)
            c = Vec2(col + map_scale.x, row + map_scale.y)
            d = Vec2(col, row + map_scale.y)

            # Add lines to the set
            lines_to_add = [(a, b), (b, c), (c, d), (d, a)]
            for line in lines_to_add:
                if not any(((line[0] == p[0] and line[1] == p[1]) or (line[0] == p[1] and line[1] == p[0])) for p in unique_lines):
                    unique_lines.append(line)
                    add_line(line[1], line[0], color, texture)
                else:
                    for o in world:
                        if (o.a == line[0] and o.b == line[1]) or (o.a == line[1] and o.b == line[0]):
                            world.remove(o)

    # Clean up the set
    del unique_lines

    exec(code)

mini_map_size = 300
fish_eye_fix = True
collision = False  # FIXME
ray_step_angle = 1 / FOV
