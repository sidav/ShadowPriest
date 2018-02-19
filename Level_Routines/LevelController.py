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
        currentLevel.set_door_closed(x, y, False)
        return True
    return False

def try_close_door(x, y):
    if currentLevel.is_door_present(x, y):
        currentLevel.set_door_closed(x, y)
        return True
    return False

def control():
    global currentLevel
    while not CW.isWindowClosed():
        player = currentLevel.get_player()
        player_looking_range = player.get_looking_range()
        player_x, player_y = player.get_position()
        peek_x, peek_y = player.get_peeking_vector()
        # LevelView.draw_absolutely_everything(currentLevel)
        if player.is_peeking():
            LevelView.draw_everything_in_LOS_from_position(currentLevel, player_x+peek_x, player_y+peek_y, player_looking_range)
        else:
            LevelView.draw_everything_in_LOS_from_position(currentLevel, player_x, player_y, player_looking_range)
        LOG.print_log()
        CW.flushConsole()
        P_C.do_key_action(currentLevel)
        A_C.pick_action_and_do(currentLevel)

