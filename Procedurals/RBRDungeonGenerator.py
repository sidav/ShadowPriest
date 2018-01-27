# Room-By-Room dungeon generator.
# Was already implemented in C# for my "StealthRoguelike" prototype.

#############################################################################
def _random(min, max): #IT'S JUST A WRAPPER. Min, max inclusive!            #
    return _rand(max-min+1)+min                                             #
                                                                            #
_LCG_X = None                                                               #
                                                                            #
def setRandomSeed(seed):                                                    # FOR TEH GREAT INDEPENDENCY!
    global _LCG_X                                                           #
    _LCG_X = seed                                                           #
                                                                            #
def _rand(mod):                                                             #
    global _LCG_X                                                           #
    if _LCG_X is None:                                                      #
        _LCG_X = 39#7355608                                                    #
    LCG_A = 14741                                                           #
    LCG_C = 757                                                             #
    LCG_M = 77777677777                                                     #
    _LCG_X = (LCG_A*_LCG_X + LCG_C) % LCG_M                                 #
    return _LCG_X%mod                                                       #
#############################################################################

_MAP_WIDTH = 80
_MAP_HEIGHT = 25

_MAX_PLACEMENT_TRIES = 1000

_MAX_CORRIDORS_COUNT = 45
_MAX_ROOMS_COUNT = 35

_MIN_ROOM_SIZE = 3
_MAX_ROOM_SIZE = 15
_MIN_CORRIDOR_LENGTH = 2
_MAX_CORRIDOR_LENGTH = 10

_FLOOR_CODE = 'floor'
_WALL_CODE = 'wall'
_DOOR_CODE = 'door'


class _Vector:
    x = y = 0

    def __init__(self, x = None, y = None):

        if x is None or y is None:
            self.x = _random(0, _MAP_WIDTH-1)
            self.y = _random(0, _MAP_HEIGHT-1)
        else:
            self.x = x
            self.y = y

####################################################


def dig(maparr, x, y, w, h, char=_FLOOR_CODE): # fill rect with char
    for i in range (x, x+w):
        for j in range (y, y+h):
            if (0 <= i < _MAP_WIDTH and 0 <= j < _MAP_HEIGHT):
                maparr[i][j] = char


def digEntryCorridor(maparr, x, y, w, h, entryX, entryY, length=0): #needed for irregular shaped rooms
    if y <= entryY <= y + h:
        if length == 0:
            length = int(w / 2)
        if entryX < x:
            dig(maparr, entryX, entryY, length, 1)
        else:
            dig(maparr, entryX - length, entryY, length, 1)
    elif x <= entryX <= x + w:
        if length == 0:
            length = int(h/2)
        if entryY < y:
            dig(maparr, entryX, entryY, 1, length)
        else:
            dig(maparr, entryX, entryY-length, 1, length)
    else:
        print("Some fuck occured at digEntryCorridor().")


def makeOutline(maparr, x, y, w, h, char=_WALL_CODE):
    for i in range(x,x+w):
        maparr[i][y] = char
        maparr[i][y+h-1] = char
    for j in range(y, y+h):
        maparr[x][j] = char
        maparr[x+w-1][j] = char


def digRoomWithInnerRoom(maparr, x, y, w, h): # digs a room with a smaller room inside
    # smallest possible bigger room is 9x9 (with walls), with 5x5 (w/walls) room inside.
    if w < 7 or h < 7: # smallest possible room is 7 WITHOUT walls counted.
        return
    innerRoomWidth = _random(5, w-2)
    innerRoomHeight = _random(5, h-2)
    innerRoomHorizOffset = _random(1, w-innerRoomWidth-1)
    innerRoomVertOffset = _random(1, h-innerRoomHeight-1)

    #first, dig the whole space.
    dig(maparr, x, y, w, h)
    #place the inner room:
    makeOutline(maparr, x+innerRoomHorizOffset, y+innerRoomVertOffset, innerRoomWidth, innerRoomHeight)
    #place the door for the inner room:
    doorIsOnUpperOrLowerWall = _random(0, 1)
    if doorIsOnUpperOrLowerWall:
        doorX = x + innerRoomHorizOffset + _random(1, innerRoomWidth-2)
        doorY = y + innerRoomVertOffset + _random(0, 1)*(innerRoomHeight - 1)
    else:
        doorY = y + innerRoomVertOffset + _random(1, innerRoomHeight - 2)
        doorX = x + innerRoomHorizOffset + _random(0, 1)*(innerRoomWidth - 1)
    maparr[doorX][doorY] = _DOOR_CODE


# def digCircularRoom(maparr, x, y, w, h, entryX, entryY): #deprecated
#     #TODO: maybe empty outer space around the room?
#     #TODO: fix wrong corridor placement into the room.
#     # w and h should be equal, odd and greater than 5.
#     # make w and h equal
#     if w < h:
#         h = w
#     else:
#         w = h
#     if w < 5 or h < 5:
#         return
#     # oddity check
#     # if w % 2 != 1:
#     #     return
#     roomRadius = int(w/2) - (w%2) # -1 # behaviour for the even w/h values may be weird.
#     if w % 2 == 0:
#         roomRadius -= 1
#     roomCenterX = x+roomRadius
#     roomCenterY = y+roomRadius
#     print("rad {0} cx {1} cy {2}".format(roomRadius, roomCenterX, roomCenterY))
#     for i in range (x, x+w):
#         for j in range (y, y+h):
#             currRelativeCoordX = i - roomCenterX
#             currRelativeCoordY = j - roomCenterY
#             if currRelativeCoordX ** 2 + currRelativeCoordY ** 2 <= roomRadius ** 2:
#                 maparr[i][j] = _FLOOR_CODE
#     digEntryCorridor(maparr, x, y, w, h, entryX, entryY, int(w/2)+1)


def digEllipticRoom(maparr, x, y, w, h, entryX, entryY):
    if w < 5 or h < 5:
        return
    roomXRadius = int(w / 2)
    roomYRadius = int(h / 2)
    if w % 2 == 0:
        roomXRadius -= 1
    if h % 2 == 0:
        roomYRadius -= 1
    entryCorrLength = (w if w > h else h)
    print("{0}, {1}".format(roomXRadius, roomYRadius))
    roomCenterX = x + roomXRadius
    roomCenterY = y + roomYRadius
    for i in range (x, x+w):
        for j in range (y, y+h):
            currRelativeCoordX = i - roomCenterX
            currRelativeCoordY = j - roomCenterY
            currXComponent = (currRelativeCoordX ** 2) * (roomYRadius ** 2)
            currYComponent = (currRelativeCoordY ** 2) * (roomXRadius ** 2)
            if currXComponent + currYComponent <= (roomXRadius ** 2) * (roomYRadius ** 2):
                maparr[i][j] = _FLOOR_CODE
    digEntryCorridor(maparr, x, y, w, h, entryX, entryY, entryCorrLength)


def digCircularOutlinedRoom(maparr, x, y, w, h, entryX, entryY): # Square room with wall circle inside.
    # w and h should be equal, odd and greater than 5.
    # make w and h equal
    if w < h:
        h = w
    else:
        w = h
    if w < 5 or h < 5:
        return
    dig(maparr, x, y, w, h)
    # oddity check
    # if w % 2 != 1:
    #     return
    roomRadius = int(w/2) - 1 # behaviour for the even w/h values may be weird.
    roomCenterX = x+roomRadius+1
    roomCenterY = y+roomRadius+1
    print("rad {0} cx {1} cy {2}".format(roomRadius, roomCenterX, roomCenterY))
    for i in range (x, x+w):
        for j in range (y, y+h):
            currRelativeCoordX = i - roomCenterX
            currRelativeCoordY = j - roomCenterY
            if currRelativeCoordX ** 2 + currRelativeCoordY ** 2 <= roomRadius ** 2 and currRelativeCoordX ** 2 + currRelativeCoordY ** 2 >= (roomRadius-1) ** 2:
                maparr[i][j] = _WALL_CODE
    digEntryCorridor(maparr, x, y, w, h, entryX, entryY)


#######
#     #
#  #  #
# ### #
#  #  #
#     #
#######
def digRoomWithCross(maparr, x, y, w, h):
    dig(maparr, x, y, w, h)
    roomMiddleX = x+int(w/2)
    roomMiddleY = y + int(h / 2)
    for i in range(x+1, x+w - 1):
        maparr[i][roomMiddleY] = _WALL_CODE
        if h % 2 == 0:
            maparr[i][roomMiddleY-1] = _WALL_CODE
    for i in range(y+1, y+h - 1):
        maparr[roomMiddleX][i] = _WALL_CODE
        if w % 2 == 0:
            maparr[roomMiddleX-1][i] = _WALL_CODE



#########
# # # # #
#       #
# # # # #
#########
def digLongRoom(maparr, x, y, w, h): #need to change the name.
    dig(maparr, x, y, w, h)
    if w < h:
        for i in range(y+1, y+h-1, 2):
            maparr[x][i] = _WALL_CODE
            maparr[x+w-1][i] = _WALL_CODE
    else:
        for i in range(x+1, x+w-1, 2):
            maparr[i][y] = _WALL_CODE
            maparr[i][y+h-1] = _WALL_CODE


###########
# #   #   #
#   #   # #
###########
def digSnakeRoom(maparr, x, y, w, h, entryX, entryY):
    obstacleWidth = 0
    dig(maparr, x, y, w, h)
    if w < h:
        obstacleWidth = w - 1
        for i in range(y+1, y+h-1, 4):
            dig(maparr, x, i, obstacleWidth, 1, _WALL_CODE)
            if i+2 < y+h:
                dig(maparr, x+w-obstacleWidth, i+2, obstacleWidth, 1, _WALL_CODE)
    else:
        obstacleWidth = h - 1
        for i in range(x+1, x+w-1, 4):
            dig(maparr, i, y, 1, obstacleWidth, _WALL_CODE)
            if i + 2 < x + w:
                dig(maparr, i+2, y+h-obstacleWidth, 1, obstacleWidth, _WALL_CODE)
    digEntryCorridor(maparr, x, y, w, h, entryX, entryY, 2)


###########################
## THERE ##################
###########################
def pickRoomAndDig(maparr, x, y, w, h, entryX, entryY):  # Subject for changes.
    #roomIsDigged = False
    roomType = _random(0, 3)
    if (w >= 7 and h >= 7):
        if roomType == 0:
            digRoomWithInnerRoom(maparr, x, y, w, h)
        elif roomType == 1:
            digEllipticRoom(maparr, x, y, w, h, entryX, entryY)
        elif roomType == 2:
            digCircularOutlinedRoom(maparr, x, y, w, h, entryX, entryY)
        elif roomType == 3:
            digRoomWithCross(maparr, x, y, w, h)
    else:
        if roomType == 1:
            digLongRoom(maparr, x, y, w, h)
        elif roomType == 2:
            digSnakeRoom(maparr, x, y, w, h, entryX, entryY)
        else: dig(maparr, x, y, w, h)
    print("room digged at ({0};{1}) with w{2}, h{3} entry({4};{5})".format(x, y, w, h, entryX, entryY))

def isWall(maparr, x, y, w=1, h=1):
    for i in range (x, x+w):
        for j in range(y, y+h):
            if 0 < i < _MAP_WIDTH-1 and 0 < j < _MAP_HEIGHT-1:
                if maparr[i][j] != _WALL_CODE:
                    return False
            else:
                return  False
    return True


def pickDirectionForDigging(maparr, x, y):
    direction = None
    if x >= _MAP_WIDTH or y >= _MAP_HEIGHT:
        print("!!!Oh noes! Coordinates cheburachnulis at ${0}, ${1}!!!".format(x, y))
        #return _Vector(0, 0)
    if maparr[x][y+1] == _FLOOR_CODE:
        direction = _Vector(0, -1)
    elif maparr[x-1][y] == _FLOOR_CODE:
        direction = _Vector(1, 0)
    elif maparr[x][y-1] == _FLOOR_CODE:
        direction = _Vector(0, 1)
    elif maparr[x+1][y] == _FLOOR_CODE:
        direction = _Vector(-1, 0)
    else:
        direction = _Vector(0, 0)
    return direction


def tryAddCorridor(maparr):
    #TODO: Maybe ALLOW corridors to lead into existing rooms?
    #TODO: i.e. disable the "corridor ending tile emptiness check"?
    for tries in range (_MAX_PLACEMENT_TRIES):
        currCell = _Vector()
        corrLength = _random(_MIN_CORRIDOR_LENGTH, _MAX_CORRIDOR_LENGTH)

        while not isWall(maparr, currCell.x, currCell.y):
            currCell = _Vector()

        digDirection = pickDirectionForDigging(maparr, currCell.x, currCell.y)
        dirx = digDirection.x
        diry = digDirection.y
        if dirx == diry == 0:
            continue

        # TODO: add dig up/down restrictions (i.e. there should be more "digged horizontally" corridors than "digged vertically" ones)
        if dirx == 1: # dig right
            if isWall(maparr, currCell.x, currCell.y-1, corrLength, 3):
                dig(maparr, currCell.x+1, currCell.y, corrLength, 1)
                maparr[currCell.x][currCell.y] = _DOOR_CODE
                return
        elif dirx == -1: # dig left
            if isWall(maparr, currCell.x-corrLength-1, currCell.y-1, corrLength, 3):
                dig(maparr, currCell.x-corrLength, currCell.y, corrLength, 1)
                maparr[currCell.x][currCell.y] = _DOOR_CODE
                return
        elif diry == 1: # dig down
            if isWall(maparr, currCell.x-1, currCell.y, 3, corrLength):
                dig(maparr, currCell.x, currCell.y+1, 1, corrLength)
                maparr[currCell.x][currCell.y] = _DOOR_CODE
                return
        elif diry == -1: # dig up
            if isWall(maparr, currCell.x-1, currCell.y-corrLength, 3, corrLength):
                dig(maparr, currCell.x, currCell.y-corrLength, 1, corrLength)
                maparr[currCell.x][currCell.y] = _DOOR_CODE
                return


def tryAddRoom(maparr):
    for tries in range (_MAX_PLACEMENT_TRIES):
        currCell = _Vector()
        roomW = _random(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
        roomH = _random(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
        horOffset = _random(0, roomW-1)
        vertOffset = _random(0, roomH-1)
        while not isWall(maparr, currCell.x, currCell.y):
            currCell = _Vector()

        digDirection = pickDirectionForDigging(maparr, currCell.x, currCell.y)
        dirx = digDirection.x
        diry = digDirection.y
        if dirx == diry == 0:
            continue
        #TODO: add dig up/down restrictions (i.e. there should be more "digged horizontally" rooms than "digged vertically" ones)
        if dirx == 1: # dig right
            if isWall(maparr, currCell.x, currCell.y-vertOffset-1, roomW+2, roomH+2):
                pickRoomAndDig(maparr, currCell.x+1, currCell.y-vertOffset, roomW, roomH, currCell.x, currCell.y)
                maparr[currCell.x][currCell.y] = _DOOR_CODE
                return
        elif dirx == -1: # dig left
            if isWall(maparr, currCell.x-roomW-1, currCell.y-vertOffset-1, roomW+2, roomH+2):
                pickRoomAndDig(maparr, currCell.x-roomW, currCell.y-vertOffset, roomW, roomH, currCell.x, currCell.y)
                maparr[currCell.x][currCell.y] = _DOOR_CODE
                return
        elif diry == 1: # dig down
            if isWall(maparr, currCell.x-horOffset-1, currCell.y, roomW+2, roomH+2):
                pickRoomAndDig(maparr, currCell.x-horOffset, currCell.y+1, roomW, roomH, currCell.x, currCell.y)
                maparr[currCell.x][currCell.y] = _DOOR_CODE
                return
        elif diry == -1: # dig up
            if isWall(maparr, currCell.x-horOffset-1, currCell.y-roomH-1, roomW+2, roomH+2):
                pickRoomAndDig(maparr, currCell.x-horOffset, currCell.y-roomH, roomW, roomH, currCell.x, currCell.y)
                maparr[currCell.x][currCell.y] = _DOOR_CODE
                return

# def findWallForDoor(maparr):
#     for _ in range(1000):
#         # first, take a look at a random cell
#         x = _random(0, _MAP_WIDTH)
#         y = _random(0, _MAP_HEIGHT)
#         # check if it's a wall
#         if maparr[x][y] != _WALL_CODE:
#             continue
#         # let's check if it is "thick" wall
#         if () or ():


def count_walls_around(maparr, x, y):
    walls = 0
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            if maparr[i][j] == _WALL_CODE:
                walls += 1
    return walls


def try_add_more_doors(maparr):
    for x in range (2, _MAP_WIDTH - 2):
        for y in range(2, _MAP_HEIGHT - 2):
            if maparr[x][y] == _FLOOR_CODE:
                curr_walls = count_walls_around(maparr, x, y)
                if curr_walls == 6:
                    chance = 15
                else:
                    chance = 95
                if curr_walls >= 6:
                    # try up
                    if maparr[x][y-2] == _FLOOR_CODE and maparr[x][y-1] == _WALL_CODE and _rand(100) < chance:
                        maparr[x][y - 1] = _DOOR_CODE
                    # down
                    if maparr[x][y+2] == _FLOOR_CODE and maparr[x][y+1] == _WALL_CODE and _rand(100) < chance:
                        maparr[x][y + 1] = _DOOR_CODE
                    # right
                    if maparr[x+2][y] == _FLOOR_CODE and maparr[x+1][y] == _WALL_CODE and _rand(100) < chance:
                        maparr[x+1][y] = _DOOR_CODE
                    # left
                    if maparr[x-2][y] == _FLOOR_CODE and maparr[x-1][y] == _WALL_CODE and _rand(100) < chance:
                        maparr[x-1][y] = _DOOR_CODE


def remove_some_doors(maparr):
    for x in range (_MAP_WIDTH):
        for y in range(_MAP_HEIGHT):
            if maparr[x][y] == _DOOR_CODE and _rand(100) < 30:
                maparr[x][y] = _FLOOR_CODE

def placeInitialRoom(maparr):
    roomW = _random(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
    roomH = _random(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
    halfRoomW = int(roomW / 2)
    halfRoomH = int(roomH / 2)
    halfMapW = int(_MAP_WIDTH / 2)
    halfMapH = int(_MAP_HEIGHT / 2)
    #pickRoomAndDig(maparr, halfMapW - halfRoomW, halfMapH - halfRoomH, roomW, roomH)
    digLongRoom(maparr, halfMapW - halfRoomW, halfMapH - halfRoomH, roomW, roomH)

def generateDungeon(mapw, maph):
    global _MAP_WIDTH, _MAP_HEIGHT
    _MAP_WIDTH = mapw
    _MAP_HEIGHT = maph
    # Fill the map with solid walls.
    maparr = [[_WALL_CODE] * (_MAP_HEIGHT + 1) for _ in range(_MAP_WIDTH + 1)]
    # Place the random room in center of the map.
    placeInitialRoom(maparr)
    #TODO: all the other shit
    currentRoomsCount = 1
    currentCorrsCount = 0
    while currentRoomsCount < _MAX_ROOMS_COUNT or currentCorrsCount < _MAX_CORRIDORS_COUNT:
        if currentCorrsCount < _MAX_CORRIDORS_COUNT:
            tryAddCorridor(maparr)
            currentCorrsCount += 1
        if currentRoomsCount < _MAX_ROOMS_COUNT:
            tryAddRoom(maparr)
            currentRoomsCount += 1

    try_add_more_doors(maparr)
    remove_some_doors(maparr)

    makeOutline(maparr, 0, 0, _MAP_WIDTH, _MAP_HEIGHT, _WALL_CODE)
    return maparr
