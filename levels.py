__author__ = 'Timothy MacDonald'
import pygame

def init_new_map():
    from constants import MAP_WIDTH, MAP_HEIGHT
    levelmap = {}
    levelmap['name'] = 'Test'
    levelmap['matrix'] = [[0 for y in range(MAP_HEIGHT)] for x in range(MAP_WIDTH)]
    for x in range(MAP_WIDTH):
        for y in range(MAP_HEIGHT):
            levelmap['matrix'][x][y] = {}
            levelmap['matrix'][x][y]['name'] = 'NOTHING'
            levelmap['matrix'][x][y]['explored'] = False
    return levelmap


def create_room(room, levelmap, theme):
    # go through the tiles in the rectangle and make them passable
    from constants import THEMES
    for x in range (room.left, room.right):
        if levelmap['matrix'][x][room.top]['name'] == 'NOTHING':
            levelmap['matrix'][x][room.top]['name'] = THEMES[theme]['wall']
        if levelmap['matrix'][x][room.bottom]['name'] == 'NOTHING':
            levelmap['matrix'][x][room.top]['name'] = THEMES[theme]['wall']
        levelmap['matrix'][x][room.bottom]['name'] = THEMES[theme]['wall']
    for y in range (room.top, room.bottom + 1):
        if levelmap['matrix'][room.left][y]['name'] == 'NOTHING':
            levelmap['matrix'][room.left][y]['name'] = THEMES[theme]['wall']
        if levelmap['matrix'][room.right][y]['name'] == 'NOTHING':
            levelmap['matrix'][room.right][y]['name'] = THEMES[theme]['wall']
    for x in range(room.left +1 , room.right):
        for y in range(room.top +1, room.bottom):
            levelmap['matrix'][x][y]['name'] = THEMES[theme]['floor']



    return levelmap


def create_h_tunnel(levelmap, theme, x1, x2, y):
    from constants import THEMES
    for x in range(min(x1, x2), max(x1, x2) + 1):
        levelmap['matrix'][x][y]['name'] = THEMES[theme]['floor']
        if levelmap['matrix'][x][y-1]['name'] == 'NOTHING':
            levelmap['matrix'][x][y-1]['name'] = THEMES[theme]['wall']
        if levelmap['matrix'][x][y+1]['name'] == 'NOTHING':
            levelmap['matrix'][x][y+1]['name'] = THEMES[theme]['wall']
    return levelmap


def create_v_tunnel(levelmap, theme, y1, y2, x):
    from constants import THEMES
    for y in range(min(y1, y2), max(y1, y2) + 1):
        levelmap['matrix'][x][y]['name'] = THEMES[theme]['floor']
        if levelmap['matrix'][x-1][y]['name'] == 'NOTHING':
            levelmap['matrix'][x-1][y]['name'] = THEMES[theme]['wall']
        if levelmap['matrix'][x+1][y]['name'] == 'NOTHING':
            levelmap['matrix'][x+1][y]['name'] = THEMES[theme]['wall']
    return levelmap


def gen_random_map():
    from constants import MAP_WIDTH, MAP_HEIGHT, MAX_ROOM_SIZE, MIN_ROOM_SIZE, MAX_ROOMS, ROOM_SPACING
    import random
    theme = 'basic'  # later we'll have multiple themes to randomize
    levelmap = init_new_map()
    rooms = []
    num_rooms = 0
    for room in range(MAX_ROOMS):
        width = random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        height = random.randrange(MIN_ROOM_SIZE, MAX_ROOM_SIZE)
        xpos = random.randrange(1, MAP_WIDTH - width -1)
        ypos = random.randrange(1, MAP_HEIGHT - height -1)
        new_room = pygame.Rect(xpos, ypos, width, height)  # use this rect to actually carve the room
        collide_room = pygame.Rect(xpos - ROOM_SPACING, ypos - ROOM_SPACING, width + ROOM_SPACING, height + ROOM_SPACING)  # use this rect for collision detection
        failed = False
        if room == 0:
            levelmap['playerstartx'] = xpos + width // 2
            levelmap['playerstarty'] = ypos + height // 2
        if collide_room.collidelist(rooms) != -1:
            failed = True
        if not failed:
            levelmap = create_room(new_room, levelmap, theme)
            room_center_x, room_center_y = new_room.center
            if not num_rooms == 0:
                prev_room_center_x, prev_room_center_y = rooms[num_rooms-1].center
                if random.randrange(0,1) == 1:
                    levelmap = create_h_tunnel(levelmap, theme, prev_room_center_x, room_center_x, prev_room_center_y)
                    levelmap = create_v_tunnel(levelmap, theme, prev_room_center_y, room_center_y, room_center_x)
                else:
                    levelmap = create_v_tunnel(levelmap, theme, prev_room_center_y, room_center_y, prev_room_center_x)
                    levelmap = create_h_tunnel(levelmap, theme, prev_room_center_x, room_center_x, room_center_y)

            rooms.append(new_room)
            num_rooms += 1
    return levelmap













