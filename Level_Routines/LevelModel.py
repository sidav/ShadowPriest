from Level_Routines.LevelTile import LevelTile as LTile
from Level_Routines.DoorTile import DoorTile
from Procedurals import RBRDungeonGenerator as RBR
from GLOBAL_DATA import Level_Tile_Data as LTD


#represents the game level (dungeon floor, etc)

class LevelModel:

    _level_map = []

    def __init__(self, mapW, mapH):
        self.generate_level(mapW, mapH)

    def pick_tile_class(self, appearance):
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
        tempMap = RBR.generateDungeon(mapW, mapH)
        for x in range(0, mapW):
            for y in range(0, mapH):
                self._level_map[x][y] = self.pick_tile_class(tempMap[x][y])

    def tile_was_seen(self, x, y):
        return self._level_map[x][y].wasSeen

    def get_tile_char(self, x, y):
        return self._level_map[x][y].get_tile_char()