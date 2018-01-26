import Routines.TdlConsoleWrapper as CW
import GLOBAL_DATA.Level_Tile_Data as DATA
import tdl


SINGLE_ARROW_MODE = False


def draw_whole_level_map(lvl): # seen tiles only
    CW.clearConsole()
    for i in range(lvl.MAP_WIDTH):
        for j in range(lvl.MAP_HEIGHT):
            currentChar = lvl.get_tile_char(i, j)
            color = DATA.get_tile_color(currentChar)
            CW.setForegroundColor(color)
            CW.putChar(currentChar, i, j)

def draw_player(lvl):
    plr = lvl.get_player()
    posx = plr.get_position()[0]
    posy = plr.get_position()[1]
    CW.setForegroundColor(200, 200, 200)
    CW.putChar(plr.get_appearance(), posx, posy)

def draw_absolutely_everything(lvl):
    draw_whole_level_map(lvl)
    draw_all_units(lvl)
    draw_player(lvl)

def get_looking_thingy_char(look_dir):
    x = look_dir[0]
    y = look_dir[1]
    if x == 0:
        return '|'
    elif y == 0:
        return '-'
    elif x * y == 1:
        return '\\'
    elif x * y == -1:
        return '/'
    else:
        print('Oh fuck, wrong looking dir! ')
        return '?'

def get_unit_arrow(look_dir):
    # Just arrows:
    if look_dir == (0, -1):
        return chr(24)
    if look_dir == (1, 0):
        return chr(26)
    if look_dir == (0, 1):
        return chr(25)
    if look_dir == (-1, 0):
        return chr(27)

    # Diagonal arrows (custom font)
    if look_dir == (1, -1):
        return chr(128)
    if look_dir == (1, 1):
        return chr(129)
    if look_dir == (-1, 1):
        return chr(130)
    if look_dir == (-1, -1):
        return chr(131)


def draw_all_units(lvl): # draws all the units regardless of LOS from player.
    # TODO: make this not crap.
    unit_list = lvl.get_all_units()
    for curr_unit in unit_list:
        CW.setForegroundColor(32, 192, 32)
        curr_appearance = curr_unit.get_appearance()
        curr_position = curr_unit.get_position()
        CW.putChar(curr_appearance, curr_position[0], curr_position[1])
        if curr_unit.has_look_direction:
            curr_look_dir = curr_unit.get_look_direction()
            if SINGLE_ARROW_MODE:
                CW.putChar(get_unit_arrow(curr_look_dir), curr_position[0],
                           curr_position[1])  # TODO: make custom font arrows optional.
            else:
                arrow_x = curr_position[0] + curr_look_dir[0]
                arrow_y = curr_position[1] + curr_look_dir[1]
                if not lvl.is_unit_present(arrow_x, arrow_y):
                    if not lvl.is_tile_passable(arrow_x, arrow_y):
                        CW.setForegroundColor(0, 0, 0)
                        CW.setBackgroundColor(32, 192, 32)
                    CW.putChar(get_unit_arrow(curr_look_dir), arrow_x, arrow_y)  # TODO: make custom font arrows optional.
                    CW.setBackgroundColor(0, 0, 0)
            #CW.putChar(get_looking_thingy_char(curr_look_dir), curr_position[0] + curr_look_dir[0], curr_position[1] + curr_look_dir[1]) # that line looks like a bullshit...
        # TODO: colors
