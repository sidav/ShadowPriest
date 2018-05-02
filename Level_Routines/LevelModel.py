import Routines.SidavRandom as rand
from GLOBAL_DATA import Level_Tile_Data as LTD
from .Level_Features.LevelTile import LevelTile as LTile
from .Player.Player import Player
from .Units.Actor import Actor
from .Items.Item import Item
from Procedurals import BSPDungeonGenerator as BSP
from Procedurals import RBRDungeonGenerator as RBR
from .Level_Features.DoorTile import DoorTile


#represents the game level (dungeon floor, etc)

class LevelModel:

    _level_map = []
    _units = []
    _items_on_floor = []
    _player = None
    _current_turn = 0

    def __init__(self, mapW, mapH):
        self.generate_level(mapW, mapH)

    def pick_tile_class(self, tile_name):
        appearance = LTD.tile_name_to_code(tile_name)
        if appearance == LTD._CLDOOR_CODE or appearance == LTD._OPDOOR_CODE:
            return DoorTile(appearance)
        else:
            return LTile(appearance)

    # generates the overworld map from the world generation routine:
    def generate_level(self, mapW, mapH):

        import time                         # <-- bad starts here
        seed = int(time.time())
        print("SEED IS {0} ".format(seed))
        BSP.setRandomSeed(seed)
        RBR.setRandomSeed(seed)             # <-- bad ends (?) here

        self.MAP_WIDTH = mapW
        self.MAP_HEIGHT = mapH
        self._level_map = [[None] * mapH for _ in range(mapW)] # <-- don't touch that fucking magic please
        tempMap = RBR.generateDungeon(mapW, mapH)
        # tempMap = BSP.generateMapWithRandomParams(mapW, mapH)
        for x in range(0, mapW):
            for y in range(0, mapH):
                self._level_map[x][y] = self.pick_tile_class(tempMap[x][y].tile_code)

    def get_tile_was_seen(self, x, y):
        return self._level_map[x][y].get_was_seen()

    def get_tile_char(self, x, y):
        return self._level_map[x][y].get_tile_char()

    def is_tile_passable(self, x, y):
        return self._level_map[x][y].get_passable() and not self.is_unit_present(x, y)

    def set_tile_was_seen(self, x, y):
        self._level_map[x][y].set_was_seen()

    def is_door_closed(self, x, y):
        if self._level_map[x][y].__class__.__name__ == 'DoorTile':
            return self._level_map[x][y].get_closed()

    def is_door_present(self, x, y):
        if self._level_map[x][y].__class__.__name__ == 'DoorTile':
            return True
        return False

    def set_door_closed(self, x, y, closed=True):
        if self._level_map[x][y].__class__.__name__ == 'DoorTile':
            self._level_map[x][y].set_closed(closed)

    def set_all_tiles_seen(self):
        for x in range(self.MAP_WIDTH):
            for y in range(self.MAP_HEIGHT):
                self.set_tile_was_seen(x, y)

    # units
    def get_unit_at(self, x, y):
        for unit in self._units:
            if (x, y) == unit.get_position():
                return unit

    def spawn_unit(self, unit):
        self._units.append(unit)

    def get_all_units(self):
        return self._units

    def is_unit_present(self, x, y):
        for unit in self._units:
            if (x, y) == unit.get_position():
                return True
        if self._player is not None and (x, y) == self._player.get_position():
            return True
        return False

    def remove_unit(self, unit):
        self._units.remove(unit)

    # /units

    # items
    def add_item_on_floor_without_cordinates(self, item):
        self._items_on_floor.append(item)

    def add_item_on_floor_at_coordinates(self, item, x, y):
        item.set_position(x, y)
        self._items_on_floor.append(item)

    def is_item_present(self, x, y):
        for item in self._items_on_floor:
            if item.get_position() == (x, y):
                return True
        return False

    def get_all_items_on_floor(self):
        return self._items_on_floor

    def get_items_at_coordinates(self, x, y):
        list_items = []
        for item in self._items_on_floor:
            if item.get_position() == (x, y):
                list_items.append(item)
        return list_items

    def get_all_bodies_on_floor(self):
        items = self._items_on_floor
        bodies = []
        for item in items:
            if item.is_body():
                bodies.append(item)
        return bodies

    def get_bodies_at_coordinates(self, x, y):
        items = self._items_on_floor
        bodies = []
        for item in items:
            if item.is_body():
                if (x, y) == item.get_position():
                    bodies.append(item)
        return bodies

    def remove_item_from_floor(self, item):
        self._items_on_floor.remove(item)
    # /items

    def get_opacity_map(self):
        mapw, maph = self.MAP_WIDTH, self.MAP_HEIGHT
        vis_map = [[None] * maph for _ in range(mapw)]
        for x in range(mapw):
            for y in range(maph):
                vis_map[x][y] = self._level_map[x][y].get_opaque()
        return vis_map

    def get_current_turn(self):
        return self._current_turn

    def next_turn(self):
        self._current_turn += 1

    def get_player(self):
        return self._player
