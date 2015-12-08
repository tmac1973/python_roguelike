__author__ = 'tim'
import sys
import json


def get_pallete_selection(palleterects, mousex, mousey):
    selection = False
    for rect in palleterects:
        if palleterects[rect].collidepoint(mousex, mousey):
            selection = rect
    return selection


def set_map_tile(levelmap, current_tile, mousex, mousey, location_x, location_y):
    validpos, mapposx, mapposy = get_map_pos(mousex, mousey, location_x, location_y)
    if validpos and current_tile:
        levelmap['matrix'][mapposx][mapposy]['name'] = current_tile


def map_editor():
    from constants import FPS, MAP_WIDTH, MAP_HEIGHT, PALLETE_OFFSET_X, PALLETE_OFFSET_Y, TILE_WIDTH, TILE_HEIGHT, \
        TILE_PALLETE_SPACING, TILE_PALLETE_ROWS, TILE_PALLETE_COLUMNS, MINIMAP_POSITION_OFFSET_X, MINIMAP_POSITION_OFFSET_Y, MINIMAP_TILE_SIZE
    from copy import deepcopy
    import os.path
    current_tile = False  # placeholder value until a tile is selected for the first time
    mapchange = True
    location_x = 0  # initial player starting xpos
    location_y = 0  # initial player starting ypos

    fpsclock = pygame.time.Clock()  # initialize the clock
    levelmap = init_new_map()  # create a new map
    oldlevelmap = deepcopy(levelmap)
    displaysurface = init_graphics()  # start pygame and build the window
    mousebuttons = pygame.mouse.get_pressed()  # get initial mouse values
    mousex, mousey = pygame.mouse.get_pos()
    bitmaps = load_tiles()  # load the tileset
    palleterects = draw_pallete(bitmaps, displaysurface)  # draw the pallet and return the button rectangles
    palleterect = pygame.Rect(PALLETE_OFFSET_X, PALLETE_OFFSET_Y,
                              (TILE_WIDTH + TILE_PALLETE_SPACING) * TILE_PALLETE_COLUMNS,
                              (TILE_HEIGHT + TILE_PALLETE_SPACING) * TILE_PALLETE_ROWS)
    # Start Main Loop
    while True:

        if mapchange:
            mapsurf = draw_main_map(levelmap, bitmaps)  # draw the main map surface
            minimapsurf = draw_mini_map(levelmap)
            mapchange = False
        displayrect = blit_map_to_main_map_surface(displaysurface, mapsurf, location_x,
                                         location_y, mousex, mousey)  # update the map portion of the screen
        minimaprect = update_mini_map_display_surface(displaysurface, minimapsurf, location_x, location_y)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_a:
                    location_x -= 1
                    if location_x < 0:
                        location_x = 0
                elif event.key == K_d:
                    location_x += 1
                    if location_x > MAP_WIDTH:
                        location_x = MAP_WIDTH
                elif event.key == K_w:
                    location_y -= 1
                    if location_y < 0:
                        location_y = 0
                elif event.key == K_s:
                    location_y += 1
                    if location_y > MAP_HEIGHT:
                        location_y = MAP_HEIGHT
                elif event.key == K_F1:
                    filename = ask(displaysurface, 'Save Filename')
                    if filename:
                        json.dump(levelmap, open(filename, 'w'))
                elif event.key == K_F2:
                    filename = ask(displaysurface, 'Load Filename')
                    if filename:
                        if os.path.isfile(filename):
                            levelmap = json.load(open(filename))
                            mapchange = True
                elif event.key == K_F3:
                    levelmap = gen_random_map()
                    mapchange = True
                elif event.key == K_ESCAPE:
                    levelmap = deepcopy(oldlevelmap)
                    mapchange = True
            if event.type == MOUSEBUTTONDOWN:
                mouse_down_x, mouse_down_y = event.pos  # store the mouse position during the click
                if displayrect.collidepoint(mouse_down_x, mouse_down_y):  # If in the map display
                    oldlevelmap = deepcopy(levelmap)  # save a copy of the level for UNDO
                if minimaprect.collidepoint(mouse_down_x, mouse_down_y):
                    location_x = (mouse_down_x - MINIMAP_POSITION_OFFSET_X) // MINIMAP_TILE_SIZE
                    location_y = (mouse_down_y - MINIMAP_POSITION_OFFSET_Y) // MINIMAP_TILE_SIZE
            if event.type == MOUSEBUTTONUP:
                if mousebuttons[0] == 1:
                    if palleterect.collidepoint(mouse_down_x, mouse_down_y):
                        old_tile = current_tile
                        current_tile = get_pallete_selection(palleterects, mouse_down_x, mouse_down_y)
                        if not current_tile:
                            current_tile = old_tile
                    if displayrect.collidepoint(mouse_down_x, mouse_down_y):
                        set_map_tile(levelmap, current_tile, mouse_down_x, mouse_down_y, location_x, location_y)
                        mapchange = True

            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                if mousebuttons[0] == 1:
                    if displayrect.collidepoint(mouse_down_x, mouse_down_y):
                        set_map_tile(levelmap, current_tile, mousex, mousey, location_x, location_y)
                        mapchange = True
        mousebuttons = pygame.mouse.get_pressed()  # store which mouse buttons were pressed
        fpsclock.tick(FPS)


def main():
    map_editor()


if __name__ == "__main__":
    from draw import draw_main_map, init_graphics, blit_map_to_main_map_surface, load_tiles, draw_pallete, ask, draw_mini_map, update_mini_map_display_surface
    from levels import init_new_map, gen_random_map
    from utils import get_map_pos
    import pygame
    from pygame.locals import *

    sys.exit(main())