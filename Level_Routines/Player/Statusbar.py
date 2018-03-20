from Routines import TdlConsoleWrapper as CW
from GLOBAL_DATA import Global_Constants as CONST

def print_statusbar(player, current_turn):
    # print player name (TODO)
    # player_name = 'Badass vile sneaky bastard priest of shadows'
    player_name = 'Priest of the Imperceptible'  # TODO: replace with actual name
    print_name_with_healthbar(player_name, player.get_current_hitpoints(), player.get_max_hitpoints())

    # print current turn
    cur_turn_str = str(current_turn)[:-1]+'.'+str(current_turn)[-1:]  # Whoa, some more fucking magic! Why fucking not?
    cur_turn_str = 'TURN: ' + cur_turn_str
    indent = len(cur_turn_str)

    CW.setForegroundColor(128, 128, 128)
    CW.putString(cur_turn_str, CONST.CONSOLE_WIDTH - indent, CONST.CONSOLE_HEIGHT - 1)


def print_name_with_healthbar(name, hp, max_hp):
    name_len = len(name)
    fraction_of_hp = float(hp) / float(max_hp)
    highlighted_hp = int(name_len * fraction_of_hp)

    hp_color = (0, 128, 0)
    # decide hp color:
    if fraction_of_hp < 0.33:
        hp_color = (128, 0, 0)
    elif fraction_of_hp <= 0.66:
        hp_color = (128, 128, 0)

    CW.putChar('[', 0, CONST.CONSOLE_HEIGHT-1)
    for i in range(name_len):
        if i <= highlighted_hp:
            CW.setBackgroundColor(hp_color)
            CW.setForegroundColor(0, 0, 0)
        else:
            CW.setBackgroundColor(0, 0, 0)
            CW.setForegroundColor(128, 128, 128)
        CW.putChar(list(name)[i], i+1, CONST.CONSOLE_HEIGHT-1)
    CW.setBackgroundColor(0, 0, 0)
    CW.setForegroundColor(128, 128, 128)
    CW.putChar(']', name_len+1, CONST.CONSOLE_HEIGHT - 1)