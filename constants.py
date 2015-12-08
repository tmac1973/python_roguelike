__author__ = 'Timothy MacDonald'
GAME_NAME = 'The GAME!'

# FPS of game
FPS = 30  # define the FPS clock

# Color Constants
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (127, 127, 127)
COLOR_DARK_GREY = (64, 64, 64)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_TRANSPARENT = (255, 0, 255)  # The tileset I use has this as the transparency color

# Graphics Rendering Constants
MAP_WIDTH = 100  # number of tiles wide each level is
MAP_HEIGHT = 100  # number of tiles high each level is
DISPLAY_WIDTH = 20 # number of tiles wide to display in main map. Must be EVEN NUMBER!
DISPLAY_HEIGHT = 20  # number of tiles high to display in main map. Must be EVEN NUMBER!
TILE_WIDTH = 32  # in pixels
TILE_HEIGHT = 32  # in pixels
TILE_PALLETE_SPACING = 4  # Space between tiles in Pallete
TILE_PALLETE_ROWS = 8
TILE_PALLETE_COLUMNS = 4
MAP_POSITION_OFFSET_X = 32  # in pixels
MAP_POSITION_OFFSET_Y = 32  # in pixels
MINIMAP_POSITION_OFFSET_X = DISPLAY_WIDTH * TILE_WIDTH + MAP_POSITION_OFFSET_X + TILE_WIDTH  # where to draw the minimap
MINIMAP_POSITION_OFFSET_Y = MAP_POSITION_OFFSET_Y
MINIMAP_TILE_SIZE = 2  # in pixes
PALLETE_OFFSET_X = DISPLAY_WIDTH * TILE_WIDTH + MAP_POSITION_OFFSET_X + TILE_WIDTH  # where to draw the pallete
PALLETE_OFFSET_Y = DISPLAY_HEIGHT // 2 * TILE_HEIGHT + TILE_HEIGHT
SCREEN_X = MAP_POSITION_OFFSET_X + DISPLAY_WIDTH * TILE_WIDTH + TILE_WIDTH * 2 + MAP_WIDTH * MINIMAP_TILE_SIZE  # screen size
SCREEN_Y = MAP_POSITION_OFFSET_Y + DISPLAY_HEIGHT * TILE_HEIGHT + TILE_HEIGHT * 2
PLAYER_INFO_SURFACE_WIDTH = 220  # in pixels
PLAYER_INFO_SURFACE_HEIGHT = 200  # in pixels
PLAYER_INFO_VERT_SPACING = 14  # in pixels
PLAYER_INFO_COLUMN_WIDTH = 100  # in pixels
PLAYER_INFO_LEFT_JUSTIFY = 10  # in pixels
PLAYER_INFO_POSITION_OFFSET_X = DISPLAY_WIDTH * TILE_WIDTH + MAP_POSITION_OFFSET_X + TILE_WIDTH  # where to draw the player info box
PLAYER_INFO_POSITION_OFFSET_Y = MAP_POSITION_OFFSET_Y + MAP_HEIGHT * MINIMAP_TILE_SIZE + 4

# map generation stuff
MAX_ROOM_SIZE = 30  # in tiles
MIN_ROOM_SIZE = 6  # in tiles
MAX_ROOMS = 70
ROOM_SPACING = 5

# Define Playable Races
RACES = {
    'HUMAN': {'str': 12,
              'int': 12,
              'dex': 12,
              'vision_radius': 5,
    }
}

# Define Playable Classes
PROFESSIONS = {
    'WARRIOR': {'strmod': 6,
                'intmod': -6,
                'dexmod': 0,
                'hpmod': 10
    }
}

# Define what tiles match with what map theme
THEMES = {
    'basic': {'floor': 'STONE_FLOOR',
              'wall': 'BRICK_WALL',
              'water': 'WATER'}
}

# Define the base level tile (floor, walls, water) types and bitmap filenames

TILES = {
    'STONE_FLOOR': {'tile': 'tiles/floor/cobble_blood1.png',
                    'type': 'FLOOR',
                    'passable': True
    },
    'NOTHING': {'tile': 'tiles/wall/nothing.png',
                'passable': False,
                'type': 'NOTHING'
    },
    'WATER': {'tile': 'tiles/floor/dngn_shallow_water.png',
              'passable': False,
              'type': 'WATER'
    },
    'BRICK_WALL': {'tile': 'tiles/wall/brick_brown0.png',
                   'passable': False,
                   'type': 'WALL'
    },
    'HUMAN_FIGHTER': {'tile': 'tiles/mobs/HumanFighter.PNG',
                      'passable': False,
                      'type': 'MOB'
    }
}
