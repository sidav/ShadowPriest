from .Item import Item
from GLOBAL_DATA.Level_Tile_Data import door_lock_level_colors, door_lock_level_names


class Key(Item):
    _stackable = False
    _lock_level = 1

    def __init__(self, posx, posy, lock_level=1):
        self._pos_x = posx
        self._pos_y = posy
        self._appearance = chr(251)
        self._name = '{} key'.format(door_lock_level_names[lock_level])
        self._weight = 1
        self._stackable = False
        self._lock_level = lock_level

    # def get_lock_level(self):
    #     return self._lock_level

    def is_of_key_level(self, key_level):
        return self._lock_level == key_level

    def get_color(self):
        return door_lock_level_colors[self._lock_level]
