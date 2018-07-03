from Routines import TdlConsoleWrapper as CW
from GLOBAL_DATA import Global_Constants as CONST, Level_Tile_Data as LTD


_statusbar_line_width = 0


def print_statusbar(player, current_turn):
    global _statusbar_line_width
    # print player name (TODO)
    # player_name = 'Badass vile sneaky bastard priest of shadows'
    player_name = ' {} '.format(player.get_name())
    print_name_with_healthbar(player_name, player.get_current_hitpoints(), player.get_max_hitpoints())

    _statusbar_line_width = len(player_name)+3

    if player.get_inventory().is_carrying_body_on_shoulder():
        CW.setForegroundColor(192, 192, 32)
        CW.putString('CARRYING BODY', len(player_name) + 3, CONST.CONSOLE_HEIGHT-1)
        _statusbar_line_width += 13
    else:
        print_keys(player)

    print_status_effects(player)

    # print current turn
    cur_turn_str = str(current_turn)[:-1]+'.'+str(current_turn)[-1:]  # Whoa, some more fucking magic! Why fucking not?
    cur_turn_str = 'TURN: ' + cur_turn_str
    indent = len(cur_turn_str)

    CW.setForegroundColor(128, 128, 128)
    CW.putString(cur_turn_str, CONST.CONSOLE_WIDTH - indent, CONST.CONSOLE_HEIGHT - 1)


def print_keys(player):
    global _statusbar_line_width
    player_name = player.get_name()
    has_any_keys = False
    for i in [1, 2]:
        if player.get_inventory().has_key_of_lock_level(i):
            CW.setBackgroundColor(LTD.door_lock_level_colors[i])
            CW.putString(' ', len(player_name) + 7 + i, CONST.CONSOLE_HEIGHT - 1)
            has_any_keys = True
    CW.setBackgroundColor(0, 0, 0)
    if has_any_keys:
        CW.putString('KEYS:', len(player_name) + 3, CONST.CONSOLE_HEIGHT - 1)
        _statusbar_line_width += 7


def print_name_with_healthbar(name, hp, max_hp):
    global _statusbar_line_width
    name_len = len(name)
    fraction_of_hp = float(hp) / float(max_hp)
    highlighted_hp = int(name_len * fraction_of_hp)

    hp_color = (0, 128, 0)
    # decide hp color:
    if fraction_of_hp == 0:
        hp_color = (0, 0, 0)
    elif fraction_of_hp < 0.33:
        hp_color = (128, 0, 0)
    elif fraction_of_hp <= 0.66:
        hp_color = (128, 128, 0)

    CW.setForegroundColor(128, 128, 128)
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


def print_status_effects(player):
    global _statusbar_line_width
    status_effects = player.get_status_effects()
    total_healing = 0
    total_poison = 0
    total_painkiller = 0
    for effect in status_effects:
        if effect.get_name() == 'HEALING':
            total_healing += 1
        if effect.get_name() == 'POISON':
            total_poison += 1
        if effect.get_name() == 'PAINKILLER':
            total_painkiller += 1

    CW.setForegroundColor(100, 100, 196)
    if total_healing == 1:
        CW.putString('HLNG', _statusbar_line_width, CONST.CONSOLE_HEIGHT-1)
        _statusbar_line_width += 4
    elif total_healing > 1:
        CW.putString('HLNG+', _statusbar_line_width, CONST.CONSOLE_HEIGHT-1)
        _statusbar_line_width += 5

    CW.setForegroundColor(90, 196, 90)
    if total_poison == 1:
        CW.putString('POIS', _statusbar_line_width, CONST.CONSOLE_HEIGHT-1)
        _statusbar_line_width += 4
    elif total_poison > 1:
        CW.putString('POIS+', _statusbar_line_width, CONST.CONSOLE_HEIGHT-1)
        _statusbar_line_width += 5

    CW.setForegroundColor(132, 32, 160)
    if total_painkiller == 1:
        CW.putString('PAINKLR', _statusbar_line_width, CONST.CONSOLE_HEIGHT-1)
        _statusbar_line_width += 7
    elif total_painkiller > 1:
        CW.putString('PAINKLR+', _statusbar_line_width, CONST.CONSOLE_HEIGHT-1)
        _statusbar_line_width += 8
