import Routines.TdlConsoleWrapper as CW
import GLOBAL_DATA.Level_Tile_Data as DATA

def draw_seen_level_map(owd): # seen tiles only
    # IS NOT IMPLEMENTED YET
    pass
    # CW.clearConsole()
    # for i in range(owd.MAP_WIDTH):
    #     for j in range(owd.MAP_HEIGHT):
    #         if owd.tile_was_seen(i, j):
    #             currentChar = owd.get_tile_char(i, j)
    #             color = DATA.getColor(currentChar)
    #             CW.setForegroundColor(color)
    #             CW.putChar(currentChar, i, j)
    #         else:
    #             CW.setForegroundColor(64, 64, 64)
    #             CW.putChar(DATA._UNEXPLORED_LAND_CODE, i, j)