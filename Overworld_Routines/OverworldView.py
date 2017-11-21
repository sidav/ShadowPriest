import Routines.TdlConsoleWrapper as CW
from Overworld_Routines.Overworld import *
import GLOBAL_DATA.Tile_Codes as DATA

# that should render the overworld and whatever

def drawAllOverworldMap(owd):
    CW.clearConsole()
    curMap = []
    curMap = owd.overworldMap
    for i in range(len(curMap)):
        for j in range(len(curMap[0])):
            currentChar = curMap[i][j]._appearance
            if currentChar != '~':
                CW.putChar(currentChar, i,j)
    CW.flushConsole()

def drawOverworldMap(owd): # seen tiles only
    CW.clearConsole()
    curMap = []
    curMap = owd.overworldMap
    for i in range(len(curMap)):
        for j in range(len(curMap[0])):
            currentChar = curMap[i][j].getAppearance()
            color = DATA.getColor(currentChar)
            if currentChar != '~':
                CW.setForegroundColor(color)
                CW.putChar(currentChar, i,j)
    CW.flushConsole()