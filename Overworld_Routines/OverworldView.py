import Routines.TdlConsoleWrapper as CW
from Overworld_Routines.OverworldModel import *
import GLOBAL_DATA.Tile_Codes as DATA

# that should render the overworld and whatever

def drawAllOverworldMap(owd):
    CW.clearConsole()
    curMap = []
    curMap = owd.overworldMap
    for i in range(len(curMap)):
        for j in range(len(curMap[0])):
            currentChar = curMap[i][j]._appearance
            CW.putChar(currentChar, i,j)
    # CW.flushConsole()

def drawSeenOverworldMap(owd): # seen tiles only
    CW.clearConsole()
    curMap = owd.overworldMap
    for i in range(len(curMap)):
        for j in range(len(curMap[0])):
            if curMap[i][j].wasSeen():
                currentChar = curMap[i][j].getAppearance()
                color = DATA.getColor(currentChar)
                CW.setForegroundColor(color)
                CW.putChar(currentChar, i, j)
            else:
                CW.setForegroundColor(64, 64, 64)
                CW.putChar(DATA._UNEXPLORED_LAND_CODE, i, j)
