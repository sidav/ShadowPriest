import GLOBAL_DATA.Level_Tile_Data as LTD
#represents one cell of a map
#TODO

class LevelTile:

    _appearance = '?'
    # __color = 0xFFFFFF #fuck
    _opaque = True # True means 'vision obstructing'
    _passable = False
    _was_seen = False

    def __init__(self, appearance):
        self._opaque = LTD.get_tile_opaque(appearance)
        self._appearance = appearance
        if appearance == LTD._FLOOR_CODE:
            self._passable = True

    def get_tile_char(self):
        return self._appearance

    def get_color(self):
        return LTD.tile_colors[self._appearance]

    def get_passable(self):
        return self._passable
    
    def get_opaque(self):
        return self._opaque

    def get_was_seen(self):
        return self._was_seen

    def set_was_seen(self, seen=True):
        self._was_seen = seen

    def is_stairs(self):
        return False
