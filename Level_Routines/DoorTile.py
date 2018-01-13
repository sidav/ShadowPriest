from .LevelTile import LevelTile
from GLOBAL_DATA import Level_Tile_Data as LTD

class DoorTile(LevelTile):

    _closed = True

    def __init__(self, appearance):
        super().__init__(appearance)
        if appearance == LTD._OPDOOR_CODE:
            self._closed = False
        elif appearance == LTD._CLDOOR_CODE:
            self._closed = True
        pass

    def get_tile_char(self):
        if self._closed:
            return '+'
        else:
            return '\\'

    def get_closed(self):
        return self._closed