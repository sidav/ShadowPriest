import Routines.TdlConsoleWrapper as CW
import GLOBAL_DATA.Level_Tile_Data as DATA

def draw_whole_level_map(lvl): # seen tiles only
    CW.clearConsole()
    for i in range(lvl.MAP_WIDTH):
        for j in range(lvl.MAP_HEIGHT):
            currentChar = lvl.get_tile_char(i, j)
            color = DATA.get_tile_color(currentChar)
            CW.setForegroundColor(color)
            CW.putChar(currentChar, i, j)

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

def draw_all_units(lvl): # draws all the units regardless of LOS from player.
    # TODO: make this not crap.
    CW.setForegroundColor(32, 192, 32)
    unit_list = lvl.get_all_units()
    for curr_unit in unit_list:
        curr_appearance = curr_unit.get_appearance()
        curr_position = curr_unit.get_position()
        CW.putChar(curr_appearance, curr_position[0], curr_position[1])
        if curr_unit.has_look_direction:
            curr_look_dir = curr_unit.get_look_direction()
            CW.putChar(get_looking_thingy_char(curr_look_dir), curr_position[0] + curr_look_dir[0], curr_position[1] + curr_look_dir[1]) # that line looks like a bullshit...
        # TODO: colors

def draw_absolutely_everything(lvl):
    draw_whole_level_map(lvl)
    draw_all_units(lvl)
