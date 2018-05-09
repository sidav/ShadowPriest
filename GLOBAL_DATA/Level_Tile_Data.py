_WALL_CODE = chr(177)
_FLOOR_CODE = '.'
_CLDOOR_CODE = '+'
_OPDOOR_CODE = '\\'
_DOWN_STAIR_CODE = '>'
_UP_STAIR_CODE = '<'

tile_names = {
    'wall': _WALL_CODE,
    'floor': _FLOOR_CODE,
    'door': _CLDOOR_CODE,
    'dstairs': _DOWN_STAIR_CODE,
    'ustairs': _UP_STAIR_CODE
}

tile_colors = {
    _WALL_CODE: (128, 128, 128),
    _FLOOR_CODE: (64, 64, 64),
    # _CLDOOR_CODE: (128, 128, 128), #door colors are now separate
    # _OPDOOR_CODE: (128, 64, 0),
    _DOWN_STAIR_CODE: (196, 128, 128),
    _UP_STAIR_CODE: (128, 128, 196)
}

door_lock_level_colors = [(128, 128, 128), (32, 196, 32), (196, 32, 32)]


door_lock_level_names = ['NULL', 'green', 'red']


tile_opaque = {
    _WALL_CODE: True,
    _FLOOR_CODE: False,
    _CLDOOR_CODE: True,
    _OPDOOR_CODE: False
}


def tile_name_to_code(word):
    return tile_names.get(word.lower(), '?')


# def get_tile_color(tile_char):
#     return tile_colors.get(tile_char, (255, 0, 255))

def get_tile_opaque(tile_char):
    return tile_opaque.get(tile_char, True)
