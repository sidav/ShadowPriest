import Routines.TdlConsoleWrapper as CW
from Overworld_Routines.OverworldModel import OverworldModel as OWM
import GLOBAL_DATA.Tile_Codes as DATA

# that should render the overworld and whatever


def draw_whole_overworld_map(owd):
    CW.clearConsole()
    curMap = []
    curMap = owd.overworldMap
    for i in range(len(curMap)):
        for j in range(len(curMap[0])):
            currentChar = curMap[i][j]._appearance
            CW.putChar(currentChar, i,j)
    # CW.flushConsole()


def draw_seen_overworld_map(owd): # seen tiles only
    CW.clearConsole()
    for i in range(owd.MAP_WIDTH):
        for j in range(owd.MAP_HEIGHT):
            if owd.tile_was_seen(i, j):
                currentChar = owd.get_tile_char(i, j)
                color = DATA.getColor(currentChar)
                CW.setForegroundColor(color)
                CW.putChar(currentChar, i, j)
            else:
                CW.setForegroundColor(64, 64, 64)
                CW.putChar(DATA._UNEXPLORED_LAND_CODE, i, j)
