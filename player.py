__author__ = 'tim'


def set_player_bitmap(player):
    if player['race'] == 'HUMAN':
        if player['class'] == 'WARRIOR':
            player['bitmap'] = 'HUMAN_FIGHTER'
    return player


def init_player(name, race, profession):
    from constants import PROFESSIONS, RACES
    from levels import gen_random_map
    from random import randint

    player = {}
    player['name'] = name
    player['race'] = race
    player['class'] = profession
    player['level'] = 1

    player['currentmaplevel'] = 0
    player['xp'] = 0
    player['str'] = RACES[player['race']]['str'] + PROFESSIONS[player['class']]['strmod']
    player['int'] = RACES[player['race']]['int'] + PROFESSIONS[player['class']]['intmod']
    player['dex'] = RACES[player['race']]['dex'] + PROFESSIONS[player['class']]['dexmod']
    player['hp'] = 1 + randint(PROFESSIONS[player['class']]['hpmod'] // 2, PROFESSIONS[player['class']]['hpmod'] )
    player['levels'] = []
    player['levels'].append(gen_random_map())
    player['locationx'] = player['levels'][0]['playerstartx']
    player['locationy'] = player['levels'][0]['playerstarty']
    player['vision_radius'] = RACES[player['race']]['vision_radius']
    player = set_player_bitmap(player)
    return player


def move_player(player, direction):
    from utils import check_adjacent_tile_passable
    # check for passable
    if direction == 'N':
        if check_adjacent_tile_passable(player, 0, -1):
            player['locationy'] -= 1
    if direction == 'NW':
        if check_adjacent_tile_passable(player, -1, -1):
            player['locationy'] -= 1
            player['locationx'] -= 1
    if direction == 'NE':
        if check_adjacent_tile_passable(player, 1, -1):
            player['locationy'] -= 1
            player['locationx'] += 1
    if direction == 'SW':
        if check_adjacent_tile_passable(player, -1, 1):
            player['locationy'] += 1
            player['locationx'] -= 1
    if direction == 'SE':
        if check_adjacent_tile_passable(player, +1, +1):
            player['locationy'] += 1
            player['locationx'] += 1
    elif direction == 'S':
        if check_adjacent_tile_passable(player, 0, +1):
            player['locationy'] += 1
    elif direction == 'W':
        if check_adjacent_tile_passable(player, -1, 0):
            player['locationx'] -= 1
    elif direction == 'E':
        if check_adjacent_tile_passable(player, +1, 0):
            player['locationx'] += 1
    return player