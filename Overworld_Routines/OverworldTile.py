import GLOBAL_DATA.Tile_Codes as CODES

#represents one tile of the global map.
class OverworldTile:
    _appearance = '?'
    _color = None
    _passable = True
    _wasSeen = False

    def __init__(self, appearance):
        self._wasSeen = False

        self._appearance = appearance


        if appearance == CODES._GROUND_CODE:
            self._color = (200, 100, 50)

        elif appearance == CODES._FOREST_CODE:
            self._color = (25, 233, 50)

        elif appearance == CODES._MOUNTAIN_CODE:
            self._passable = False
            self._color = (128, 128, 128)

        elif appearance == CODES._WATER_CODE:
            self._passable = False

    def get_appearance(self):
        return self._appearance

    def was_seen(self):
        return bool(self._wasSeen)

    def set_seen(self, seenBool):
        self._wasSeen = seenBool

    def is_passable(self):
        return self._passable