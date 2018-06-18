from .LevelTile import LevelTile
from GLOBAL_DATA import Level_Tile_Data as LTD
from ..Minigames.Lockpick import Lockpick

class DoorTile(LevelTile):

    _closed = True
    _lock_level = 0
    _lockpicking_minigame = None

    def __init__(self, appearance, lock_level=0):
        super().__init__(appearance)
        if appearance == LTD._OPDOOR_CODE:
            self._closed = False
        elif appearance == LTD._CLDOOR_CODE:
            self._closed = True
        self._lock_level = lock_level
        if lock_level == 1:
            self._lockpicking_minigame = Lockpick(3, 3)
        elif lock_level == 2:
            self._lockpicking_minigame = Lockpick(4, 3)

    def get_tile_char(self):
        if self._closed:
            return '+'
        else:
            return '\\'

    def get_lockpicking_minigame(self):
        return self._lockpicking_minigame

    def get_color(self):
        return LTD.door_lock_level_colors[self._lock_level]

    def set_closed(self, closed=True):
        self._closed = closed
        if self._lockpicking_minigame is not None:
            self._lockpicking_minigame.reset_state()

    def get_closed(self):
        return self._closed

    def get_passable(self):
        return not self._closed

    def get_opaque(self):
        return self._closed
