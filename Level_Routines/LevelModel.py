from .LevelTile import LevelTile as LTile
from .DoorTile import DoorTile
from .Unit import Unit
from .Actor import Actor
from .Player import Player
from Procedurals import BSPDungeonGenerator as BSP
from Procedurals import RBRDungeonGenerator as RBR
from GLOBAL_DATA import Level_Tile_Data as LTD

import Routines.SidavRandom as rand


#represents the game level (dungeon floor, etc)

class LevelModel:

    _level_map = []
    _units = []
    _player = None

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
        RBR.setRandomSeed(seed)             # <-- bad ends (?) here

        self.MAP_WIDTH = mapW
        self.MAP_HEIGHT = mapH
        self._level_map = [[None] * mapH for _ in range(mapW)] # <-- don't touch that fucking magic please
        # tempMap = RBR.generateDungeon(mapW, mapH)
        tempMap = BSP.generateMapWithRandomParams(mapW, mapH)
        for x in range(0, mapW):
            for y in range(0, mapH):
                self._level_map[x][y] = self.pick_tile_class(tempMap[x][y])

        self.place_random_units()
        self.place_player()

    def get_tile_was_seen(self, x, y):
        return self._level_map[x][y].get_was_seen()

    def get_tile_char(self, x, y):
        return self._level_map[x][y].get_tile_char()

    def get_all_units(self):
        return self._units

    def is_tile_passable(self, x, y):
        return self._level_map[x][y].get_passable()

    def set_tile_was_seen(self, x, y):
        self._level_map[x][y].set_was_seen()

    def set_all_tiles_seen(self):
        for x in range(self.MAP_WIDTH):
            for y in range(self.MAP_HEIGHT):
                self.set_tile_was_seen(x, y)

    def is_unit_present(self, x, y):
        # TODO: Check for the player?..
        for unit in self._units:
            if (x, y) == unit.get_position():
                return True
        return False

    def get_opacity_map(self):
        mapw, maph = self.MAP_WIDTH, self.MAP_HEIGHT
        vis_map = [[None] * maph for _ in range(mapw)]
        for x in range(mapw):
            for y in range(maph):
                vis_map[x][y] = self._level_map[x][y].get_opaque()
        return vis_map


    def get_player(self):
        return self._player

    def place_player(self):
        posx = posy = 0
        while not (self.is_tile_passable(posx, posy)):
            posx = rand.rand(self.MAP_WIDTH)
            posy = rand.rand(self.MAP_HEIGHT)
        self._player = Player(posx, posy)

    def place_random_units(self): # <- FUCKING TEMPORARY # TODO: REMOVE
        # rand.randomize()
        for _ in range(10):
            posx = posy = 0
            while not (self.is_tile_passable(posx, posy)):
                posx = rand.rand(self.MAP_WIDTH)
                posy = rand.rand(self.MAP_HEIGHT)
            self._units.append(Actor(posx, posy, 'G'))
