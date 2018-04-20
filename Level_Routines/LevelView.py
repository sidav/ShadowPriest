import Routines.TdlConsoleWrapper as CW
import GLOBAL_DATA.Level_Tile_Data as DATA
from Routines import SidavLOS as LOS
import tdl


SINGLE_ARROW_MODE = False
NON_VISIBLE_TILE_COLOR = (32, 32, 64)

map_of_already_drawn_items = []

def draw_whole_level_map(lvl): # seen tiles only
    CW.clearConsole()
    for i in range(lvl.MAP_WIDTH):
        for j in range(lvl.MAP_HEIGHT):
            currentChar = lvl.get_tile_char(i, j)
            color = DATA.get_tile_color(currentChar)
            CW.setForegroundColor(color)
            CW.putChar(currentChar, i, j)


def draw_only_level_map_in_LOS(lvl, vis_table):
    for i in range(lvl.MAP_WIDTH):
        for j in range(lvl.MAP_HEIGHT):
            currentChar = lvl.get_tile_char(i, j)
            draw_this_tile = False
            if vis_table[i][j]:
                color = DATA.get_tile_color(currentChar)
                lvl.set_tile_was_seen(i, j)
                draw_this_tile = True
            elif lvl.get_tile_was_seen(i, j):
                color = NON_VISIBLE_TILE_COLOR
                draw_this_tile = True
            if draw_this_tile:
                CW.setForegroundColor(color)
                CW.putChar(currentChar, i, j)


def draw_player(lvl):
    plr = lvl.get_player()
    posx = plr.get_position()[0]
    posy = plr.get_position()[1]
    CW.setForegroundColor(200, 200, 200)
    CW.putChar(plr.get_appearance(), posx, posy)


def draw_all_units(lvl): # draws all the units regardless of LOS from player.
    # TODO: make this not crap.
    unit_list = lvl.get_all_units()
    for curr_unit in unit_list:
        draw_unit_itself_only(lvl, curr_unit)
        if curr_unit.has_look_direction:
            draw_unit_look_direction_only(lvl, curr_unit)


def draw_absolutely_everything(lvl):
    draw_whole_level_map(lvl)
    draw_all_units(lvl)
    draw_player(lvl)


def draw_everything_in_LOS_from_position(lvl, px, py, looking_range=1):
    global map_of_already_drawn_items
    map_w = lvl.MAP_WIDTH  # bad?
    map_h = lvl.MAP_HEIGHT  # bad?
    map_of_already_drawn_items = [[False] * map_h for _ in range(map_w)]  # bad?

    CW.clearConsole()
    opacity_map = lvl.get_opacity_map()
    vis_map = LOS.getVisibilityTableFromPosition(px, py, opacity_map, looking_range)
    # print(opacity_map)
    draw_only_level_map_in_LOS(lvl, vis_map)
    draw_items_in_visibility_map(lvl, vis_map)
    draw_bodies_in_visibility_map(lvl, vis_map)
    draw_units_in_visibility_map(lvl, vis_map)
    draw_player(lvl)


def draw_units_in_visibility_map(lvl, vis_map):
    unit_list = lvl.get_all_units()
    for curr_unit in unit_list:
        ux, uy = curr_unit.get_position()
        if vis_map[ux][uy]:
            draw_unit_itself_only(lvl, curr_unit)
            if curr_unit.has_look_direction:
                draw_unit_look_direction_only(lvl, curr_unit)


def draw_items_in_visibility_map(lvl, vis_map):  # skips bodies!
    global map_of_already_drawn_items
    item_list = lvl.get_all_items_on_floor()
    for curr_item in item_list:
        if curr_item.is_body():
            continue
        ix, iy = curr_item.get_position()
        if vis_map[ix][iy]:
            inverse = map_of_already_drawn_items[ix][iy]
            draw_item(curr_item, inverse)
            map_of_already_drawn_items[ix][iy] = True


def draw_bodies_in_visibility_map(lvl, vis_map):
    body_list = lvl.get_all_bodies_on_floor()
    for body in body_list:
        ix, iy = body.get_position()
        if vis_map[ix][iy]:
            inverse = map_of_already_drawn_items[ix][iy]
            draw_item(body, inverse)
            map_of_already_drawn_items[ix][iy] = True

# ---------------------------------------------------------------------------------------------------------- #


def draw_item(item, inverse=False):
    CW.setForegroundColor(item.get_color())
    if inverse:
        CW.setForegroundColor(0, 0, 0)
        CW.setBackgroundColor(item.get_color())
    curr_appearance = item.get_appearance()
    curr_position = item.get_position()
    CW.putChar(curr_appearance, curr_position[0], curr_position[1])
    if inverse:
        CW.setBackgroundColor(0, 0, 0)


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


def draw_unit_itself_only(lvl, curr_unit):
    # TODO: colors.
    curr_appearance = curr_unit.get_appearance()
    curr_position = curr_unit.get_position()
    if lvl.is_item_present(curr_position[0], curr_position[1]):
        CW.setForegroundColor(0, 0, 0)
        CW.setBackgroundColor(curr_unit.get_color())
    else:
        CW.setForegroundColor(curr_unit.get_color())
    CW.putChar(curr_appearance, curr_position[0], curr_position[1])


def draw_unit_look_direction_only(lvl, curr_unit):
    curr_position = curr_unit.get_position()
    curr_look_dir = curr_unit.get_look_direction()
    if SINGLE_ARROW_MODE:
        CW.putChar(get_unit_arrow(curr_look_dir), curr_position[0],
                   curr_position[1])  # TODO: make custom font arrows optional.
    else:
        arrow_x = curr_position[0] + curr_look_dir[0]
        arrow_y = curr_position[1] + curr_look_dir[1]
        if not lvl.is_unit_present(arrow_x, arrow_y):
            if not lvl.is_tile_passable(arrow_x, arrow_y) or lvl.is_item_present(arrow_x, arrow_y):
                CW.setForegroundColor(0, 0, 0)
                CW.setBackgroundColor(curr_unit.get_color())
            CW.putChar(get_unit_arrow(curr_look_dir), arrow_x, arrow_y)  # TODO: make custom font arrows optional.
            CW.setBackgroundColor(0, 0, 0)
    # CW.putChar(get_looking_thingy_char(curr_look_dir), curr_position[0] + curr_look_dir[0], curr_position[1] + curr_look_dir[1]) # that line looks like a bullshit...
