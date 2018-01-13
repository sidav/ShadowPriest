from Routines import TdlConsoleWrapper as CW
from GLOBAL_DATA import Global_Constants as GC
from Level_Routines.LevelModel import LevelModel
from Level_Routines import LevelView

player_x = player_y = 0
last_tile = '.'
currentLevel = None

def initialize():
    currentLevel = LevelModel(GC.MAP_WIDTH, GC.MAP_HEIGHT)
    # LevelView.draw_whole_level_map(currentLevel)
    LevelView.draw_absolutely_everything(currentLevel)
    placePlayer()
    CW.flushConsole()
    CW.readKey()

def control():
    pass

def placePlayer():
    pass