import Routines.TdlConsoleWrapper as CW
from Overworld_Routines.Overworld import *

# that should render the overworld and whatever

def drawAllOverworldMap(owd: Overworld):
    CW.clearConsole()
    curMap = []
    curMap = owd.overworldMap
    for i in range(len(curMap)):
        for j in range(len(curMap[0])):
            currentChar = curMap[i][j]._appearance
            if currentChar != '~':
                CW.putChar(currentChar, i,j)
    CW.flushConsole()

def drawOverworldMap(owd: Overworld): # seen tiles only
    CW.clearConsole()
    curMap = []
    curMap = owd.overworldMap
    for i in range(len(curMap)):
        for j in range(len(curMap[0])):
            currentChar = curMap[i][j]._appearance
            if currentChar != '~':
                CW.putChar(currentChar, i,j)
    CW.flushConsole()