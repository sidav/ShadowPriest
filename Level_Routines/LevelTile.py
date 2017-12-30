import GLOBAL_DATA.Level_Tile_Data as LTD
#represents one cell of a map
#TODO

class LevelTile:

    _appearance = '?'
    __color = 0xFFFFFF #fuck
    _vision_obstructing = True
    _passable = False

    def __init__(self, appearance):
        self._appearance = appearance
        if appearance == LTD._WALL_CODE:
            self._color = LTD._WALL_COLOR

        elif appearance == LTD._FLOOR_CODE:
            self._color = LTD._FLOOR_COLOR
            self._passable = True

        elif appearance == LTD._DOOR_CODE:
            self._color = LTD._DOOR_COLOR # TODO: fucking doors.
    
    def get_passable(self):
        return self._passable
    
    def get_vision_obstructing(self):
        return self._vision_obstructing