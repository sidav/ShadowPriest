from .LevelTile import LevelTile
from GLOBAL_DATA import Level_Tile_Data as LTD

class DoorTile(LevelTile):

    _closed = True
    _lock_level = 0

    def __init__(self, appearance, lock_level=0):
        super().__init__(appearance)
        if appearance == LTD._OPDOOR_CODE:
            self._closed = False
        elif appearance == LTD._CLDOOR_CODE:
            self._closed = True
        self._lock_level = lock_level

    def get_tile_char(self):
        if self._closed:
            return '+'
        else:
            return '\\'

    def get_color(self):
        return LTD.door_lock_level_colors[self._lock_level]

    def get_lock_level(self):
        return self._lock_level

    def set_closed(self, closed=True):
        self._closed = closed

    def get_closed(self):
        return self._closed

    def get_passable(self):
        return not self._closed

    def get_opaque(self):
        return self._closed
