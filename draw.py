__author__ = 'tim'
import pygame
from pygame.locals import *


def display_box(screen, message):
    """Print a message in a box in the middle of the screen"""
    fontobject = pygame.font.Font(None, 18)
    pygame.draw.rect(screen, (0, 0, 0),
                     ((screen.get_width() / 2) - 100,
                      (screen.get_height() / 2) - 10,
                      200, 20), 0)
    pygame.draw.rect(screen, (255, 255, 255),
                     ((screen.get_width() / 2) - 102,
                      (screen.get_height() / 2) - 12,
                      204, 24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                    ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.update()


def ask(screen, question):
    """ask(screen, question) -> answer"""
    from utils import get_key

    pygame.font.init()
    current_string = ''
    display_box(screen, question + ": " + current_string)
    while 1:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
        elif inkey == K_RETURN:
            break
        elif inkey == K_ESCAPE:
            return False
        elif inkey <= 127:
            current_string += chr(inkey)
        display_box(screen, question + ": " + current_string)
    return current_string


def draw_pallete(bitmaps, displaysurface):
    from constants import PALLETE_OFFSET_X, PALLETE_OFFSET_Y, TILE_HEIGHT, TILE_WIDTH, TILES, COLOR_WHITE, \
        TILE_PALLETE_SPACING

    def draw_pallete_button(x, y):
        boxrect = pygame.Rect(x - 2, y - 2, TILE_WIDTH + 4, TILE_HEIGHT + 4)
        pygame.draw.rect(displaysurface, COLOR_WHITE, boxrect, 1)
        pygame.display.update(boxrect)
        palleterects[name] = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
        displaysurface.blit(bitmaps[name]['tile'], palleterects[name])
        pygame.display.update(palleterects[name])

    number_of_walls = 0
    number_of_floors = 0
    palleterects = {}  # dictionary that stores location and name of pallete tiles
    x = PALLETE_OFFSET_X  # position the pallete on screen
    y = PALLETE_OFFSET_Y  # position the pallete on screen
    for name in bitmaps:  # for every loaded bitmap draw first pallete column
        if TILES[name]['type'] == 'FLOOR' or TILES[name][
            'type'] == 'WATER':  # test if it's a floor tile to draw in the first pallete column
            draw_pallete_button(x + TILE_WIDTH + TILE_PALLETE_SPACING,
                                y + ((TILE_HEIGHT + TILE_PALLETE_SPACING) * number_of_floors))
            number_of_floors += 1
        if TILES[name]['type'] == 'WALL' or TILES[name][
            'type'] == 'NOTHING':  # test if it's a wall tile to draw in the second column
            draw_pallete_button(x, y + ((TILE_HEIGHT + TILE_PALLETE_SPACING) * number_of_walls))
            number_of_walls += 1
    return palleterects


def init_graphics():
    from constants import SCREEN_X, SCREEN_Y, GAME_NAME, COLOR_BLACK

    pygame.init()
    displaySurface = pygame.display.set_mode((SCREEN_X, SCREEN_Y), HWSURFACE | DOUBLEBUF)
    print('Display surface bitdepth is: {0}\n'.format(displaySurface.get_bitsize()))
    pygame.display.set_caption(GAME_NAME)
    displaySurface.fill(COLOR_BLACK)
    return displaySurface


def load_tiles():
    from constants import TILES, TILE_WIDTH, TILE_HEIGHT

    bitmaps = {}
    for name in TILES:
        bitmaps[name] = {}
        bitmaps[name]['tile'] = pygame.image.load(TILES[name]['tile']).convert()
        bitmaps[name]['tile'] = pygame.transform.scale(bitmaps[name]['tile'], (TILE_WIDTH, TILE_HEIGHT))
        #if TILES[name]['type'] == 'MOB':
        #    bitmaps[name]['tile'].set_colorkey(COLOR_TRANSPARENT)

    return bitmaps


def init_main_map_surface():
    from constants import MAP_WIDTH, MAP_HEIGHT, TILE_WIDTH, TILE_HEIGHT, DISPLAY_WIDTH, DISPLAY_HEIGHT
    mapsurfwidth = (MAP_WIDTH * TILE_WIDTH) + (DISPLAY_WIDTH * TILE_WIDTH)  # xtra size is for borders
    mapsurfheight = (MAP_HEIGHT * TILE_HEIGHT) + (DISPLAY_HEIGHT * TILE_HEIGHT)  # xtra size is for borders
    mapsurf = pygame.Surface((mapsurfwidth, mapsurfheight))
    return mapsurf


def init_mini_map_surface():
    from constants import MAP_WIDTH, MAP_HEIGHT, MINIMAP_TILE_SIZE
    minimapsurfwidth = MAP_WIDTH * MINIMAP_TILE_SIZE
    minimapsurfheight = MAP_HEIGHT * MINIMAP_TILE_SIZE
    minimapsurf = pygame.Surface((minimapsurfwidth, minimapsurfheight))
    return minimapsurf


def init_player_info_surface():
    from constants import PLAYER_INFO_SURFACE_WIDTH, PLAYER_INFO_SURFACE_HEIGHT
    playerinfosurf = pygame.Surface((PLAYER_INFO_SURFACE_WIDTH, PLAYER_INFO_SURFACE_HEIGHT))
    return playerinfosurf


def draw_player_info_box(player, playerinfosurf):
    from constants import PLAYER_INFO_COLUMN_WIDTH, PLAYER_INFO_VERT_SPACING, COLOR_WHITE, \
                        PLAYER_INFO_SURFACE_WIDTH, PLAYER_INFO_SURFACE_HEIGHT, PLAYER_INFO_LEFT_JUSTIFY
    fontobject = pygame.font.Font(None, 18)
    inforect = pygame.Rect(0,0, PLAYER_INFO_SURFACE_WIDTH, PLAYER_INFO_SURFACE_HEIGHT)
    pygame.draw.rect(playerinfosurf, COLOR_WHITE, inforect, 1 )
    x = PLAYER_INFO_LEFT_JUSTIFY
    y = PLAYER_INFO_VERT_SPACING
    info = 'Name: ' + player['name']
    playerinfosurf.blit(fontobject.render(info, 0, COLOR_WHITE),( x, y))
    y = y + PLAYER_INFO_VERT_SPACING
    info = 'Race: ' + player['race']
    playerinfosurf.blit(fontobject.render(info, 0, COLOR_WHITE),( x, y))
    y = y + PLAYER_INFO_VERT_SPACING
    info = 'Class: ' + player['class']
    playerinfosurf.blit(fontobject.render(info, 0, COLOR_WHITE),( x, y))
    y = y + PLAYER_INFO_VERT_SPACING
    info = 'STR: ' + str(player['str'])
    playerinfosurf.blit(fontobject.render(info, 0, COLOR_WHITE),( x, y))
    y = y + PLAYER_INFO_VERT_SPACING
    info = 'INT: ' + str(player['int'])
    playerinfosurf.blit(fontobject.render(info, 0, COLOR_WHITE),( x, y))
    y = y + PLAYER_INFO_VERT_SPACING
    info = 'DEX: ' + str(player['dex'])
    playerinfosurf.blit(fontobject.render(info, 0, COLOR_WHITE),( x, y))
    y = y + PLAYER_INFO_VERT_SPACING
    info = 'HP: ' + str(player['hp'])
    playerinfosurf.blit(fontobject.render(info, 0, COLOR_WHITE),( x, y))
    y = y + PLAYER_INFO_VERT_SPACING
    info = 'XP: ' + str(player['xp'])
    playerinfosurf.blit(fontobject.render(info, 0, COLOR_WHITE),( x, y))
    return playerinfosurf


def update_player_info_box(displaysurface, playerinfosurf):
    from constants import PLAYER_INFO_POSITION_OFFSET_X, PLAYER_INFO_POSITION_OFFSET_Y, PLAYER_INFO_SURFACE_WIDTH, PLAYER_INFO_SURFACE_HEIGHT
    playerinforect = pygame.Rect(PLAYER_INFO_POSITION_OFFSET_X, PLAYER_INFO_POSITION_OFFSET_Y, PLAYER_INFO_SURFACE_WIDTH, PLAYER_INFO_SURFACE_HEIGHT)
    displaysurface.set_clip(playerinforect)
    displaysurface.blit(playerinfosurf, playerinforect)
    pygame.display.update(playerinforect)
    return playerinforect


def draw_mini_map(player, minimapsurf, drawfull):
    from constants import TILES, MAP_WIDTH, MAP_HEIGHT, MINIMAP_TILE_SIZE, COLOR_BLACK, COLOR_DARK_GREY, COLOR_GREY, \
        COLOR_BLUE
    if drawfull:
        for tilex in range(MAP_WIDTH):
            for tiley in range(MAP_HEIGHT):
                if player['levels'][player['currentmaplevel']]['matrix'][tilex][tiley]['explored']:
                    tilerect = pygame.Rect(tilex * MINIMAP_TILE_SIZE, tiley * MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE,
                                           MINIMAP_TILE_SIZE)
                    if TILES[player['levels'][player['currentmaplevel']]['matrix'][tilex][tiley]['name']]['type'] == 'NOTHING':
                        pygame.draw.rect(minimapsurf, COLOR_BLACK, tilerect, 0)
                    elif TILES[player['levels'][player['currentmaplevel']]['matrix'][tilex][tiley]['name']]['type'] == 'WALL':
                        pygame.draw.rect(minimapsurf, COLOR_GREY, tilerect, 0)
                    elif TILES[player['levels'][player['currentmaplevel']]['matrix'][tilex][tiley]['name']]['type'] == 'WATER':
                        pygame.draw.rect(minimapsurf, COLOR_BLUE, tilerect, 0)
                    elif TILES[player['levels'][player['currentmaplevel']]['matrix'][tilex][tiley]['name']]['type'] == 'FLOOR':
                        pygame.draw.rect(minimapsurf, COLOR_DARK_GREY, tilerect, 0)
    else:
        for tilex in range(player['locationx'] - player['vision_radius'], player['locationx'] + player['vision_radius']):
            for tiley in range(player['locationy'] - player['vision_radius'], player['locationy'] + player['vision_radius']):
                if player['levels'][player['currentmaplevel']]['matrix'][tilex][tiley]['explored']:
                    tilerect = pygame.Rect(tilex * MINIMAP_TILE_SIZE, tiley * MINIMAP_TILE_SIZE, MINIMAP_TILE_SIZE,
                                           MINIMAP_TILE_SIZE)
                    if TILES[player['levels'][player['currentmaplevel']]['matrix'][tilex][tiley]['name']]['type'] == 'NOTHING':
                        pygame.draw.rect(minimapsurf, COLOR_BLACK, tilerect, 0)
                    elif TILES[player['levels'][player['currentmaplevel']]['matrix'][tilex][tiley]['name']]['type'] == 'WALL':
                        pygame.draw.rect(minimapsurf, COLOR_GREY, tilerect, 0)
                    elif TILES[player['levels'][player['currentmaplevel']]['matrix'][tilex][tiley]['name']]['type'] == 'WATER':
                        pygame.draw.rect(minimapsurf, COLOR_BLUE, tilerect, 0)
                    elif TILES[player['levels'][player['currentmaplevel']]['matrix'][tilex][tiley]['name']]['type'] == 'FLOOR':
                        pygame.draw.rect(minimapsurf, COLOR_DARK_GREY, tilerect, 0)
    return minimapsurf


def update_mini_map_display_surface(displaysurface, minimapsurface, locationx, locationy):
    from constants import MINIMAP_POSITION_OFFSET_X, MINIMAP_POSITION_OFFSET_Y, MAP_WIDTH, MAP_HEIGHT, \
        MINIMAP_TILE_SIZE, COLOR_WHITE, DISPLAY_WIDTH, DISPLAY_HEIGHT

    minimaprect = pygame.Rect(MINIMAP_POSITION_OFFSET_X, MINIMAP_POSITION_OFFSET_Y, MAP_WIDTH * MINIMAP_TILE_SIZE,
                              MAP_HEIGHT * MINIMAP_TILE_SIZE)
    visiblearearect = pygame.Rect(
        MINIMAP_POSITION_OFFSET_X + locationx * MINIMAP_TILE_SIZE - DISPLAY_WIDTH // 2 * MINIMAP_TILE_SIZE,
        MINIMAP_POSITION_OFFSET_Y + locationy * MINIMAP_TILE_SIZE - DISPLAY_WIDTH // 2 * MINIMAP_TILE_SIZE,
        DISPLAY_WIDTH * MINIMAP_TILE_SIZE, DISPLAY_HEIGHT * MINIMAP_TILE_SIZE)
    displaysurface.set_clip(minimaprect)
    displaysurface.blit(minimapsurface, minimaprect)
    pygame.draw.rect(displaysurface, COLOR_WHITE, visiblearearect, 1)
    pygame.display.update(minimaprect)
    return minimaprect


def highlight_tile(displaysurface, mousex, mousey, locationx, locationy):
    from utils import get_display_pos, get_map_pos
    from constants import COLOR_GREY, MAP_POSITION_OFFSET_X, MAP_POSITION_OFFSET_Y, TILE_WIDTH, TILE_HEIGHT

    tilex, tiley = get_display_pos(mousex, mousey)
    valid_tile, mapposx, mapposy = get_map_pos(mousex, mousey, locationx, locationy)
    if valid_tile:
        hilightrect = (
            MAP_POSITION_OFFSET_X + tilex * TILE_WIDTH, MAP_POSITION_OFFSET_Y + tiley * TILE_HEIGHT, TILE_WIDTH,
            TILE_HEIGHT)
        pygame.draw.rect(displaysurface, COLOR_GREY, hilightrect, 1)
        pygame.display.update(hilightrect)


def draw_main_map(player, bitmaps, mapsurf, drawfull):
    from constants import MAP_WIDTH, MAP_HEIGHT, TILE_WIDTH, TILE_HEIGHT, DISPLAY_WIDTH, DISPLAY_HEIGHT

    if drawfull:
        for x_index in range(0, MAP_WIDTH):
            for y_index in range(0, MAP_HEIGHT):
                if player['levels'][player['currentmaplevel']]['matrix'][x_index][y_index]['explored']:
                    name = player['levels'][player['currentmaplevel']]['matrix'][x_index][y_index]['name']
                    x = ((x_index + DISPLAY_WIDTH // 2) * TILE_WIDTH)
                    y = ((y_index + DISPLAY_HEIGHT // 2) * TILE_HEIGHT)
                    # print('X:{0} Y:{1}'.format(x,y))
                    spacerect = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
                    mapsurf.blit(bitmaps[name]['tile'], spacerect)
    else:
        for x_index in range(player['locationx'] - player['vision_radius'], player['locationx'] + player['vision_radius']):
            for y_index in range(player['locationy'] - player['vision_radius'], player['locationy'] + player['vision_radius']):
                if player['levels'][player['currentmaplevel']]['matrix'][x_index][y_index]['explored']:
                    name = player['levels'][player['currentmaplevel']]['matrix'][x_index][y_index]['name']
                    x = ((x_index + DISPLAY_WIDTH // 2) * TILE_WIDTH)
                    y = ((y_index + DISPLAY_HEIGHT // 2) * TILE_HEIGHT)
                    # print('X:{0} Y:{1}'.format(x,y))
                    spacerect = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
                    mapsurf.blit(bitmaps[name]['tile'], spacerect)
    return mapsurf


def get_mob_display_coords_in_pixels_based_on_player_location(locationx, locationy, playerlocationx, playerlocationy):
    from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_WIDTH, TILE_HEIGHT
    relativex = (locationx + DISPLAY_HEIGHT // 2 - playerlocationx) % DISPLAY_WIDTH
    relativey = (locationy + DISPLAY_WIDTH // 2 - playerlocationy) % DISPLAY_HEIGHT
    x = relativex * TILE_WIDTH
    y = relativey * TILE_HEIGHT
    print(locationx % DISPLAY_WIDTH)
    return x,y


def draw_mobs(player, bitmaps):
    from constants import DISPLAY_WIDTH, DISPLAY_HEIGHT, TILE_WIDTH, TILE_HEIGHT, COLOR_TRANSPARENT
    mobsurfwidth = DISPLAY_WIDTH * TILE_WIDTH
    mobsurfheight = DISPLAY_HEIGHT * TILE_HEIGHT
    mobsurf = pygame.Surface((mobsurfwidth, mobsurfheight))
    mobsurf.fill(COLOR_TRANSPARENT)
    mobsurf.set_colorkey(COLOR_TRANSPARENT)
    x, y = DISPLAY_WIDTH // 2 * TILE_WIDTH, DISPLAY_HEIGHT // 2 * TILE_HEIGHT
    playerrect = pygame.Rect(x, y, TILE_WIDTH, TILE_HEIGHT)
    mobsurf.blit(bitmaps[player['bitmap']]['tile'], playerrect)
    return mobsurf


def update_main_display_surface(displaysurface, mapsurf, mobsurf, mousex, mousey, location_x, location_y):
    from constants import MAP_POSITION_OFFSET_X, MAP_POSITION_OFFSET_Y, DISPLAY_WIDTH, DISPLAY_HEIGHT
    from constants import TILE_HEIGHT, TILE_WIDTH
    displayrect = pygame.Rect(MAP_POSITION_OFFSET_X, MAP_POSITION_OFFSET_Y, DISPLAY_WIDTH * TILE_WIDTH,
                              DISPLAY_HEIGHT * TILE_HEIGHT)
    area = pygame.Rect(location_x * TILE_WIDTH, location_y * TILE_HEIGHT, DISPLAY_WIDTH * TILE_WIDTH, DISPLAY_HEIGHT * TILE_HEIGHT)  # compute the are from the main map to draw on screen
    displaysurface.set_clip(displayrect)
    displaysurface.blit(mapsurf, displayrect, area)  # blit the base map to screen
    displaysurface.blit(mobsurf, displayrect)  # blit the mobs on top of the base map
    pygame.display.update(displayrect)
    if displayrect.collidepoint(mousex, mousey):
        highlight_tile(displaysurface, mousex, mousey, location_x, location_y)
    return displayrect



