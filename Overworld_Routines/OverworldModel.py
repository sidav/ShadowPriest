import ShadowPriest as Main
import Procedurals.CALandscapeGenerator as MapGenerator
from Overworld_Routines.OverworldTile import OverworldTile as OTile
#from ShadowPriest import MAP_WIDTH, MAP_HEIGHT


#Represents the global map.
class OverworldModel:
    _overworldMap = []

    MAP_WIDTH = MAP_HEIGHT = 0

    def __init__(self, mapW, mapH):
        self.generateOverworld(mapW, mapH)

    def setTilesVisible(self, x, y):
        for i in [x-1, x, x+1]:
            for j in [y-1, y, y+1]:
                if (0 <= i < self.MAP_WIDTH) and (0 <= j < self.MAP_HEIGHT):
                    self._overworldMap[i][j].set_seen(True)

    def tile_is_passable(self, x, y):
        return self._overworldMap[x][y].is_passable()

    def tile_was_seen(self, x, y):
        return self._overworldMap[x][y].was_seen()

    def get_tile_char(self, x, y):
        return self._overworldMap[x][y].get_appearance()

    #generates the overworld map from the world generation routine:
    def generateOverworld(self, mapW, mapH):
        self.MAP_WIDTH = mapW
        self.MAP_HEIGHT = mapH
        self._overworldMap = [[None] * mapH for _ in range(mapW)]
        tempMap = MapGenerator.generateMap(mapW, mapH)
        for x in range(0, mapW):
           for y in range(0, mapH):
               print("Current xy: {0},{1}".format(x, y))
               self._overworldMap[x][y] = OTile(tempMap[x][y])