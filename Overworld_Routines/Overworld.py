import ShadowPriest as Main
import Procedurals.CALandscapeGenerator as MapGenerator
import Overworld_Routines.OverworldTile as OTile
from ShadowPriest import MAP_WIDTH, MAP_HEIGHT


#Represents the global map.
class Overworld:
    overworldMap = [[None] * MAP_WIDTH for _ in range(MAP_HEIGHT)]

    #generates the overworld map from the world generation routine:
    def generateOverworld(self):
        tempMap = MapGenerator.doCALandshit()
        for x in range(0, Main.MAP_WIDTH):
           for y in range(0, Main.MAP_HEIGHT):
               self.overworldMap[x][y] =OTile(tempMap[x][y])