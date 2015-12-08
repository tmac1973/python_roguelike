__author__ = 'tim'
from pygame.locals import *


def make_all_explored(player):
    from constants import MAP_WIDTH, MAP_HEIGHT

    for x in range(0, MAP_WIDTH):
        for y in range(0, MAP_HEIGHT):
            player['levels'][player['currentmaplevel']]['matrix'][x][y]['explored'] = True
    return player


def check_adjacent_tile_passable(player, x, y):
    from constants import TILES

    newx = player['locationx'] + x
    newy = player['locationy'] + y
    return TILES[player['levels'][player['currentmaplevel']]['matrix'][newx][newy]['name']]['passable']


def is_point_visible_by_player(player, x, y):
    from math import pow

    if pow(x - player['locationx'], 2) + pow(y - player['locationy'], 2) < pow(player['vision_radius'], 2):
        return True
    else:
        return False


def update_explored_portion_of_map_based_on_vision(player):
    from constants import MAP_WIDTH, MAP_HEIGHT

    xmin = player['locationx'] - player['vision_radius']
    xmax = player['locationx'] + player['vision_radius']
    ymin = player['locationy'] - player['vision_radius']
    ymax = player['locationy'] + player['vision_radius']
    if xmin < 0:
        xmin = 0
    if ymin < 0:
        ymin = 0
    if xmax >= MAP_WIDTH:
        xmax = MAP_WIDTH - 1
    if ymax >= MAP_HEIGHT:
        ymax = MAP_HEIGHT - 1
    for x in range(xmin, xmax):
        for y in range(ymin, ymax):
            if is_point_visible_by_player(player, x, y):
                player['levels'][player['currentmaplevel']]['matrix'][x][y]['explored'] = True
    return player


def get_display_pos(mousex, mousey):
    from constants import MAP_POSITION_OFFSET_X, MAP_POSITION_OFFSET_Y, TILE_HEIGHT, TILE_WIDTH

    xtilepos = (mousex - MAP_POSITION_OFFSET_X) // TILE_WIDTH
    ytilepos = (mousey - MAP_POSITION_OFFSET_Y) // TILE_HEIGHT
    return xtilepos, ytilepos


def get_map_pos(mousex, mousey, locationx, locationy):
    from constants import MAP_WIDTH, MAP_HEIGHT, DISPLAY_WIDTH, DISPLAY_HEIGHT

    valid = False
    xpos, ypos = get_display_pos(mousex, mousey)
    mapposx = locationx - DISPLAY_WIDTH // 2 + xpos
    mapposy = locationy - DISPLAY_HEIGHT // 2 + ypos
    if 0 <= mapposx < (MAP_WIDTH - 1) and 0 <= mapposy < (MAP_HEIGHT - 1):
        valid = True
    return valid, mapposx, mapposy


def get_key():
    import pygame

    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            return event.key
        else:
            pass