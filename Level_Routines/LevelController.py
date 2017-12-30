from GLOBAL_DATA import Global_Constants as GC
from Level_Routines.LevelModel import LevelModel
from Level_Routines import LevelView

player_x = player_y = 0
last_tile = '.'
currentLevel = None

def initialize():
    currentWorld = LevelModel(GC.MAP_WIDTH, GC.MAP_HEIGHT)
    placePlayer()

def control():
    pass

def placePlayer():
    pass