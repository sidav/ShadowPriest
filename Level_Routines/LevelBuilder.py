from Tile import Tile
import Procedurals.RBRDungeonGenerator as RBRGen
#This thing gets the map from some procedural generation routine, finalizes it and makes the level instance for the map.
#TODO

_FLOOR_CODE = ' '
_WALL_CODE = '#'
_DOOR_CODE = '+'

def _getBasicLevel(mapW, mapH): #makes the "skeleton" of the level from some procedural generation routine.
    #RBRGen.setTileCodes(_FLOOR_CODE, _WALL_CODE, _DOOR_CODE)
    basicMap = RBRGen.generateDungeon()#generateMapWithRandomParams(mapW, mapH)
    readyMap = [[None]*mapH for _ in range(mapW)]
    for i in range(mapW):
        for j in range(mapH):
            if basicMap[i][j] == _FLOOR_CODE:
                readyMap[i][j] = Tile(' ', True, False)
            if basicMap[i][j] == _WALL_CODE:
                readyMap[i][j] = Tile('#', False, True)
            if basicMap[i][j] == _DOOR_CODE:
                readyMap[i][j] = Tile(' ', False, False)
    return readyMap