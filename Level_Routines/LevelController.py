from Message_Log import MessageLog as LOG
from Routines import TdlConsoleWrapper as CW
from GLOBAL_DATA import Global_Constants as GC
from .LevelModel import LevelModel
from . import LevelView
from . import PlayerController as P_C
from . import ActorController as A_C

player_x = player_y = 0
last_tile = '.'
currentLevel = None

def initialize():
    global currentLevel
    currentLevel = LevelModel(GC.MAP_WIDTH, GC.MAP_HEIGHT)


def try_open_door(x, y):
    if currentLevel.is_door_present(x, y):
        currentLevel.
    return False


def control():
    global currentLevel
    while not CW.isWindowClosed():
        # LevelView.draw_absolutely_everything(currentLevel)
        LevelView.draw_everything_in_player_LOS(currentLevel)
        LOG.print_log()
        CW.flushConsole()
        P_C.do_key_action(currentLevel)
        A_C.pick_action_and_do(currentLevel)

