from Routines import TdlConsoleWrapper as CW
from GLOBAL_DATA import Global_Constants as CONST, Level_Tile_Data as LTD


_statusbar_line_width = 0


def print_statusbar(player, current_turn):
    global _statusbar_line_width
    _statusbar_line_width = 0
    # print player name (TODO)
    # player_name = 'Badass vile sneaky bastard priest of shadows'
    player_name = ' {} '.format(player.get_name())
    print_name_with_healthbar(player_name, player.get_current_hitpoints(), player.get_max_hitpoints())

    if player.get_inventory().is_carrying_body_on_shoulder():
        CW.setForegroundColor(192, 192, 32)
        CW.putString('CARRYING BODY', _statusbar_line_width, CONST.CONSOLE_HEIGHT-1)
        _statusbar_line_width += 14
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
    keys_line = 'KEYS:'
    total_keys = 0
    for i in [1, 2]:
        if player.get_inventory().has_key_of_lock_level(i):
            CW.setBackgroundColor(LTD.door_lock_level_colors[i])
            CW.putString(' ', _statusbar_line_width + len(keys_line) + i - 1, CONST.CONSOLE_HEIGHT - 1)
            total_keys += 1
    CW.setBackgroundColor(0, 0, 0)
    if total_keys > 0:
        CW.putString(keys_line, _statusbar_line_width, CONST.CONSOLE_HEIGHT - 1)
        _statusbar_line_width += len(keys_line) + total_keys + 1


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
    _statusbar_line_width += len(name) + 3


def print_status_effects(player):
    global _statusbar_line_width

    if player.is_hidden_in_shadow():
        CW.setForegroundColor(100, 32, 192)
        add_status_line('SHDW')

    if player.is_peeking():
        CW.setForegroundColor(100, 100, 0)
        add_status_line('PEEK')

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

    if total_healing > 0:
        CW.setForegroundColor(100, 100, 196)
        status_line = 'HLNG' if total_healing == 1 else 'HLNG+'
        add_status_line(status_line)

    if total_poison > 0:
        CW.setForegroundColor(90, 196, 90)
        status_line = 'POIS' if total_poison == 1 else 'POIS+'
        add_status_line(status_line)

    if total_painkiller > 0:
        CW.setForegroundColor(132, 32, 160)
        status_line = 'PNKLR' if total_painkiller == 1 else 'PNKLR+'
        add_status_line(status_line)


def add_status_line(line):
    global _statusbar_line_width
    CW.putString(line, _statusbar_line_width, CONST.CONSOLE_HEIGHT - 1)
    _statusbar_line_width += len(line)
