# MVC, anyone?
import Routines.TdlConsoleWrapper as CW
import GLOBAL_DATA.Global_Constants as GC
from Overworld_Routines.OverworldModel import OverworldModel as OW
import Overworld_Routines.OverworldView as OW_View

player_x = player_y = 0
currentWorld = OW(GC.MAP_WIDTH, GC.MAP_HEIGHT)

def initialize():
    currentWorld = OW(GC.MAP_WIDTH, GC.MAP_HEIGHT)
    placePlayer()

def placePlayer(): #stub. SHOULD BE IN MODEL OR something
    global player_x, player_y
    for i in range(currentWorld.MAP_WIDTH):
        for j in range(currentWorld.MAP_HEIGHT):
            if currentWorld.tile_is_passable(i, j):
                player_x, player_y = i, j
                return


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



def doKeyWork(keyPressed): # stub
    key = keyPressed.text
    global player_x, player_y
    vector_x = vector_y = 0
    if key == 'h':
        print("zomg")
        vector_x -= 1
    elif key == 'j':
        vector_y += 1
    elif key == 'k':
        vector_y -= 1
    elif key == 'l':
        vector_x += 1
    elif key == 'y':
        vector_x -= 1
        vector_y -= 1
    elif key == 'u':
        vector_x += 1
        vector_y -= 1
    elif key == 'b':
        vector_x -= 1
        vector_y += 1
    elif key == 'n':
        vector_x += 1
        vector_y += 1
    if currentWorld.tile_is_passable(player_x + vector_x, player_y + vector_y):
        player_x += vector_x
        player_y += vector_y