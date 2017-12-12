# MVC, anyone?
import Routines.TdlConsoleWrapper as CW
import GLOBAL_DATA.Global_Constants as GC
from Overworld_Routines.Overworld import Overworld as OW
import Overworld_Routines.OverworldView as OW_View

player_x = player_y = 0
currentWorld = OW(GC.MAP_WIDTH, GC.MAP_HEIGHT)

def initialize():
    currentWorld = OW(GC.MAP_WIDTH, GC.MAP_HEIGHT)

def control():
    global player_x, player_y
    while 1:
        currentWorld.setTilesVisible(player_x, player_y)
        OW_View.drawSeenOverworldMap(currentWorld)
        CW.setForegroundColor(200, 200, 200)
        CW.putChar('@', player_x, player_y)
        CW.flushConsole()
        keyPressed = CW.readKey()
        doKeyWork(keyPressed)



def doKeyWork(keyPressed):
    key = keyPressed.text
    global player_x, player_y
    if key == 'h':
        print("zomg")
        player_x -= 1
    elif key == 'j':
        player_y += 1
    elif key == 'k':
        player_y -= 1
    elif key == 'l':
        player_x += 1
    elif key == 'y':
        player_x -= 1
        player_y -= 1
    elif key == 'u':
        player_x += 1
        player_y -= 1
    elif key == 'b':
        player_x -= 1
        player_y += 1
    elif key == 'n':
        player_x += 1
        player_y += 1
