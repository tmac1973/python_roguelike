__author__ = 'Timothy MacDonald'


def main():
    from player import init_player
    from draw import init_graphics, load_tiles
    from loop import main_loop
    player = init_player('Tim', 'HUMAN', 'WARRIOR')
    # player['locationx'] = 0
    # player['locationy'] = 0
    displaysurface = init_graphics()  # start pygame and build the window
    bitmaps = load_tiles()
    main_loop(player, displaysurface, bitmaps)
    print(player)


main()