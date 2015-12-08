__author__ = 'tim'
import pygame
from pygame.locals import *


def main_loop(player, displaysurface, bitmaps):
    from constants import FPS, MINIMAP_POSITION_OFFSET_X, \
        MINIMAP_POSITION_OFFSET_Y, MINIMAP_TILE_SIZE
    from draw import draw_main_map, draw_mini_map, update_mini_map_display_surface, draw_mobs, \
        ask, update_main_display_surface, init_main_map_surface, init_mini_map_surface, init_player_info_surface, \
        draw_player_info_box, update_player_info_box
    from player import move_player
    from utils import update_explored_portion_of_map_based_on_vision, make_all_explored
    import os.path
    import json
    import sys

    mapchangeall = True  # redraw the entire explored map surface the first time
    mapchange = True
    fpsclock = pygame.time.Clock()  # initialize the clock
    mousebuttons = pygame.mouse.get_pressed()  # get initial mouse values
    mousex, mousey = pygame.mouse.get_pos()
    mapsurf = init_main_map_surface()
    minimapsurf = init_mini_map_surface()
    playinfosurf = init_player_info_surface()
    # Start Main Loop
    while True:

        player = update_explored_portion_of_map_based_on_vision(player)

        if mapchangeall:
            mapsurf = draw_main_map(player, bitmaps, mapsurf, True)  # redraw the entire explored main map surface
            minimapsurf = draw_mini_map(player, minimapsurf, True)
            mapchangeall = False
        if mapchange:
            mapsurf = draw_main_map(player, bitmaps, mapsurf, False)  # draw the main map surface in view of the player
            minimapsurf = draw_mini_map(player, minimapsurf, False)
            mapchange = False

        mobsurf = draw_mobs(player, bitmaps)
        displayrect = update_main_display_surface(displaysurface, mapsurf, mobsurf, mousex, mousey, player['locationx'],
                                                  player['locationy'])
        minimaprect = update_mini_map_display_surface(displaysurface, minimapsurf, player['locationx'],
                                                      player['locationy'])
        playinfosurf = draw_player_info_box(player, playinfosurf)
        playinforect = update_player_info_box(displaysurface, playinfosurf)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                if event.key == K_UP:
                    player = move_player(player, 'N')
                    mapchange = True
                elif event.key == K_DOWN:
                    player = move_player(player, 'S')
                    mapchange = True
                elif event.key == K_LEFT:
                    player = move_player(player, 'W')
                    mapchange = True
                elif event.key == K_RIGHT:
                    player = move_player(player, 'E')
                    mapchange = True
                elif event.key == K_F1:
                    filename = ask(displaysurface, 'Save Filename')
                    if filename:
                        json.dump(player, open(filename, 'w'))
                elif event.key == K_F2:
                    filename = ask(displaysurface, 'Load Filename')
                    if filename:
                        if os.path.isfile(filename):
                            player = json.load(open(filename))
                            mapchangeall = True
                elif event.key == K_F12:
                    player = make_all_explored(player)
                    mapchangeall = True
            if event.type == MOUSEBUTTONDOWN:
                mouse_down_x, mouse_down_y = event.pos  # store the mouse position during the click
                if displayrect.collidepoint(mouse_down_x, mouse_down_y):  # If in the map display
                    None
                if minimaprect.collidepoint(mouse_down_x, mouse_down_y):
                    player['locationx'] = (mouse_down_x - MINIMAP_POSITION_OFFSET_X) // MINIMAP_TILE_SIZE
                    player['locationy'] = (mouse_down_y - MINIMAP_POSITION_OFFSET_Y) // MINIMAP_TILE_SIZE
            if event.type == MOUSEBUTTONUP:
                if mousebuttons[0] == 1:
                    None
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                if mousebuttons[0] == 1:
                    if displayrect.collidepoint(mouse_down_x, mouse_down_y):
                        None
        mousebuttons = pygame.mouse.get_pressed()  # store which mouse buttons were pressed
        fpsclock.tick(FPS)