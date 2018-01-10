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
