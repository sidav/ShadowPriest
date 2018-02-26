from GLOBAL_DATA import Global_Constants as GC
from .Player import PlayerController as P_C, Statusbar
from .Units import ActorController as A_C
from Message_Log import MessageLog as LOG
from Routines import TdlConsoleWrapper as CW
from . import LevelView
from .LevelModel import LevelModel

player_x = player_y = 0
last_tile = '.'
redraw_map_timeout = 10
DEFAULT_REDRAW_MAP_TIMEOUT = 10
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


def is_time_to_act(unit):
    current_turn = currentLevel.get_current_turn()
    if unit.get_next_turn_to_act() <= current_turn:
        return True
    return False

def is_item_present(x, y):
    return currentLevel.is_item_present(x, y)

def get_items_at_coordinates(x, y):
    return currentLevel.get_items_at_coordinates(x, y)


def try_pick_up_item(unit, item):
    x, y = unit.get_position()
    ix, iy = item.get_position()
    if (x, y) == (ix, iy):
        unit.get_inventory().add_item(item)
        currentLevel.remove_item_from_floor(item)
        return True
    else:
        return False


def try_drop_item(unit, item):
    x, y = unit.get_position()
    unit.get_inventory().remove_item(item)
    currentLevel.add_item_on_floor_at_coordinates(item, x, y)
    return True


def control():
    global currentLevel, redraw_map_timeout
    player = currentLevel.get_player()

    while not CW.isWindowClosed():
        player_looking_range = player.get_looking_range()
        player_x, player_y = player.get_position()
        peek_x, peek_y = player.get_peeking_vector()

        all_units = currentLevel.get_all_units()

        current_turn = currentLevel.get_current_turn()
        # do we need to redraw the map?
        if redraw_map_timeout == 0 or is_time_to_act(player):
            # LevelView.draw_absolutely_everything(currentLevel)
            if player.is_peeking():
                LevelView.draw_everything_in_LOS_from_position(currentLevel, player_x+peek_x, player_y+peek_y, player_looking_range)
            else:
                LevelView.draw_everything_in_LOS_from_position(currentLevel, player_x, player_y, player_looking_range)
            LOG.print_log()
            Statusbar.print_statusbar(current_turn)
            CW.flushConsole()
            redraw_map_timeout = DEFAULT_REDRAW_MAP_TIMEOUT

        if is_time_to_act(player):
            P_C.do_key_action(currentLevel)
        for unit in all_units:
            if is_time_to_act(unit):
                A_C.control(currentLevel, unit)
        currentLevel.next_turn()
        redraw_map_timeout -= 1