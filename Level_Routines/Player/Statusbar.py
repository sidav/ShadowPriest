from Routines import TdlConsoleWrapper as CW
from GLOBAL_DATA import Global_Constants as CONST

def print_statusbar(current_turn):
    # print player name (TODO)
    player_name = 'Badass vile sneaky bastard priest of shadows'
    CW.setForegroundColor(128, 128, 128)
    CW.putString(player_name, 0, CONST.CONSOLE_HEIGHT - 1)

    # print current turn
    cur_turn_str = str(current_turn)[:-1]+'.'+str(current_turn)[-1:]  # Whoa, some more fucking magic! Why fucking not?
    cur_turn_str = 'TURN: ' + cur_turn_str
    indent = len(cur_turn_str)

    CW.setForegroundColor(128, 128, 128)
    CW.putString(cur_turn_str, CONST.CONSOLE_WIDTH - indent, CONST.CONSOLE_HEIGHT - 1)
