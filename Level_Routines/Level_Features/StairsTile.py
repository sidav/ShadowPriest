from .LevelTile import LevelTile
from GLOBAL_DATA import Level_Tile_Data as LTD


class StairsTile(LevelTile):

    def __init__(self, appearance, lock_level):
        super().__init__(appearance, lock_level)

    def get_passable(self):
        return True

    def get_opaque(self):
        return True

    def is_stairs(self):
        return True

    def is_upstairs(self):
        return self._appearance == LTD._UP_STAIR_CODE

    def get_stairs_name(self):
        if self._appearance == LTD._DOWN_STAIR_CODE:
            return 'stairs leading down'
        elif self._appearance == LTD._UP_STAIR_CODE:
            return 'stairs leading up'
        else:
            return 'some glitched stairs'