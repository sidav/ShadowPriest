_WALL_CODE = chr(177)
_FLOOR_CODE = '.'
_CLDOOR_CODE = '+'
_OPDOOR_CODE = '\\'

tile_names = {
    'wall': _WALL_CODE,
    'floor': _FLOOR_CODE,
    'door': _CLDOOR_CODE
}

tile_colors = {
    _WALL_CODE: (128, 128, 128),
    _FLOOR_CODE: (64, 64, 64),
    _CLDOOR_CODE: (128, 128, 128),
    _OPDOOR_CODE: (128, 64, 0)
}

tile_opaque = {
    _WALL_CODE: True,
    _FLOOR_CODE: False,
    _CLDOOR_CODE: True,
    _OPDOOR_CODE: False
}


def tile_name_to_code(word):
    return tile_names.get(word.lower(), '?')


def get_tile_color(tile_char):
    return tile_colors.get(tile_char, (255, 0, 255))

def get_tile_opaque(tile_char):
    return tile_opaque.get(tile_char, True)
