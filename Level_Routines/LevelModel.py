from GLOBAL_DATA import Level_Tile_Data as LTD
from Procedurals import RBRDungeonGenerator as RBR
from Level_Routines.LevelTile import LevelTile as LTile

#represents the game level (dungeon floor, etc)

class LevelModel:

    _level_map = []

    def __init__(self, mapW, mapH):
        self.generate_level(mapW, mapH)

    # generates the overworld map from the world generation routine:
    def generate_level(self, mapW, mapH):
        self.MAP_WIDTH = mapW
        self.MAP_HEIGHT = mapH
        self._level_map = [[None] * mapH for _ in range(mapW)] # <-- don't touch that fucking magic please
        tempMap = RBR.generateDungeon(mapW, mapH)
        for x in range(0, mapW):
            for y in range(0, mapH):
                print("Current xy: {0},{1}".format(x, y))
                self._level_map = LTile(tempMap[x][y])