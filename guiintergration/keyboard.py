from enum import Enum

import pygame


class Keys(Enum):
    KEY_Q = pygame.K_q
    KEY_W = pygame.K_w
    KEY_E = pygame.K_e
    KEY_R = pygame.K_r
    KEY_T = pygame.K_t
    KEY_Y = pygame.K_y
    KEY_U = pygame.K_u
    KEY_I = pygame.K_i
    KEY_O = pygame.K_o
    KEY_P = pygame.K_p
    KEY_A = pygame.K_a
    KEY_S = pygame.K_s
    KEY_D = pygame.K_d
    KEY_F = pygame.K_f
    KEY_G = pygame.K_g
    KEY_H = pygame.K_h
    KEY_J = pygame.K_j
    KEY_K = pygame.K_k
    KEY_L = pygame.K_l
    KEY_Z = pygame.K_z
    KEY_X = pygame.K_x
    KEY_C = pygame.K_c
    KEY_V = pygame.K_v
    KEY_B = pygame.K_b
    KEY_N = pygame.K_n
    KEY_M = pygame.K_m
    KEY_LEFT = pygame.K_LEFT
    KEY_RIGHT = pygame.K_RIGHT
    KEY_UP = pygame.K_UP
    KEY_DOWN = pygame.K_DOWN
    KEY_LSHIFT = pygame.K_LSHIFT
    KEY_RSHIFT = pygame.K_RSHIFT
    KEY_LCTRL = pygame.K_LCTRL
    KEY_RCTRL = pygame.K_RCTRL
    KEY_TAB = pygame.K_TAB
    KEY_ESC = pygame.K_ESCAPE
    KEY_DEL = pygame.K_DELETE
    KEY_BACKSPACE = pygame.K_BACKSPACE
    KEY_ENTER = pygame.K_KP_ENTER


def get_pressed(key: Keys):
    return pygame.key.get_pressed()[key.value]
