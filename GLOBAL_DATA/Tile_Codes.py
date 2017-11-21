_WATER_CODE = '~'
_WATER_COLOR = (10, 10, 240)
_GROUND_CODE = '.'
_GROUND_COLOR = (200, 100, 0)
_MOUNTAIN_CODE = '^'
_MOUNTAIN_COLOR = (192, 192, 192)
_FOREST_CODE = 'f'
_FOREST_COLOR = (10, 240, 10)
_FIELD_CODE = '"'
_FIELD_COLOR = (200, 200, 0)
_TOWN_CODE = 'O'
_TOWN_COLOR = (255, 255, 255)
_MILITARY_BASE_CODE = '%'
_MILITARY_BASE_COLOR = (200, 0, 0)
_LAB_CODE = '&'
_LAB_COLOR = (100, 0, 255)


def getColor(code):
    if code == _WATER_CODE:
        color = _WATER_COLOR
    elif code == _GROUND_CODE:
        color = _GROUND_COLOR
    elif code == _MOUNTAIN_CODE:
        color = _MOUNTAIN_COLOR
    elif code == _FOREST_CODE:
        color = _FOREST_COLOR
    elif code == _FIELD_CODE:
        color = _FIELD_COLOR
    else:
        color = (255, 0, 255)
        print("Unknown color for the tile '{0}'".format(code))
    return color
