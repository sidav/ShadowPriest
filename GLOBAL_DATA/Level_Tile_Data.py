_WALL_CODE = '#'
_WALL_COLOR = (128, 64, 0)
_FLOOR_CODE = ' '
_FLOOR_COLOR = (200, 200, 200)
_CLDOOR_CODE = '+'
_OPDOOR_CODE = '\\'

tile_colors = {
    _WALL_CODE: (128, 128, 128),
    _FLOOR_CODE: (200, 200, 200),
    _CLDOOR_CODE: (128, 128, 128),
    _OPDOOR_CODE: (128, 64, 0)
}

tile_opaque = {
    _WALL_CODE: True,
    _FLOOR_CODE: False,
    _CLDOOR_CODE: True,
    _OPDOOR_CODE: False
}


def get_tile_color(tile_char):
    return tile_colors.get(tile_char, (255, 0, 255))

def get_tile_opaque(tile_char):
    return tile_opaque.get(tile_char, True)
