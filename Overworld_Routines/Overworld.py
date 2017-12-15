import ShadowPriest as Main
import Procedurals.CALandscapeGenerator as MapGenerator
from Overworld_Routines.OverworldTile import OverworldTile as OTile
#from ShadowPriest import MAP_WIDTH, MAP_HEIGHT


#Represents the global map.
class Overworld:
    overworldMap = []

    MAP_WIDTH = MAP_HEIGHT = 0

    def __init__(self, mapW, mapH):
        self.generateOverworld(mapW, mapH)

    def setTilesVisible(self, x, y):
        for i in [x-1, x, x+1]:
            for j in [y-1, y, y+1]:
                if (0 <= i < self.MAP_WIDTH) and (0 <= j < self.MAP_HEIGHT):
                    self.overworldMap[i][j].setSeen(True)

    #generates the overworld map from the world generation routine:
    def generateOverworld(self, mapW, mapH):
        self.MAP_WIDTH = mapW
        self.MAP_HEIGHT = mapH
        self.overworldMap = [[None] * mapH for _ in range(mapW)]
        tempMap = MapGenerator.generateMap(mapW, mapH)
        for x in range(0, mapW):
           for y in range(0, mapH):
               print("Current xy: {0},{1}".format(x, y))
               self.overworldMap[x][y] = OTile(tempMap[x][y])