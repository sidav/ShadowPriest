# Room-By-Room dungeon generator v0.3
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

_MAX_ROOM_PLACEMENT_TRIES = 1000
_MAX_CORRIDOR_PLACEMENT_TRIES = 500

_MAX_CORRIDORS_COUNT = 50
_MAX_ROOMS_COUNT = 50

_MIN_ROOM_SIZE = 2
_MAX_ROOM_SIZE = 15
_MIN_CORRIDOR_LENGTH = 2
_MAX_CORRIDOR_LENGTH = 15

_FLOOR_CODE = 'floor'
_WALL_CODE = 'wall'
_DOOR_CODE = 'door'
_KEY_KEEPER_CODE = 'kkeeper'
_DOWN_STAIRS_CODE = 'dstairs'
_UP_STAIRS_CODE = 'ustairs'

_DEBUG_TILE_CODE = 'debugtile'

curr_key_level = 0
max_key_level = 2

current_map = []


class Tile:
    tile_code = 'wall'
    key_level = 0
    
    def __init__(self, char, key_level=curr_key_level):
        self.tile_code = char
        self.key_level = key_level


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


def put_single_tile(x, y, char_code=_FLOOR_CODE, key_level=-1):
    global current_map
    if key_level == -1:
        key_level = curr_key_level
    current_map[x][y] = Tile(char_code, key_level)


def put_rect_of_tiles(x, y, w, h, char=_FLOOR_CODE, key_level=-1):  # fill rect with char
    global current_map
    if key_level == -1:
        key_level = curr_key_level
    for i in range (x, x+w):
        for j in range (y, y+h):
            if 0 <= i < _MAP_WIDTH and 0 <= j < _MAP_HEIGHT:
                current_map[i][j] = Tile(char, key_level)


def digEntryCorridor(x, y, w, h, entryX, entryY, length=0): #needed for irregular shaped rooms
    global current_map
    if y <= entryY <= y + h:
        if length == 0:
            length = int(w / 1.5)
        if entryX < x:
            put_rect_of_tiles(entryX, entryY, length, 1)
        else:
            put_rect_of_tiles(entryX - length, entryY, length, 1)
    elif x <= entryX <= x + w:
        if length == 0:
            length = int(h/2)
        if entryY < y:
            put_rect_of_tiles(entryX, entryY, 1, length)
        else:
            put_rect_of_tiles(entryX, entryY - length, 1, length)
    else:
        print("Some fuck occured at digEntryCorridor().")


def makeOutline(x, y, w, h, char=_WALL_CODE, key_level=-1):
    global current_map
    for i in range(x,x+w):
        put_single_tile(i, y, char, key_level)
        put_single_tile(i, y+h-1, char, key_level)
    for j in range(y, y+h):
        put_single_tile(x, j, char, key_level)
        put_single_tile(x+w-1, j, char, key_level)


def digRoomWithInnerRoom(x, y, w, h): # digs a room with a smaller room inside
    global current_map
    # smallest possible bigger room is 9x9 (with walls), with 5x5 (w/walls) room inside.
    if w < 7 or h < 7: # smallest possible room is 7 WITHOUT walls counted.
        return
    innerRoomWidth = _random(5, w-2)
    innerRoomHeight = _random(5, h-2)
    innerRoomHorizOffset = _random(1, w-innerRoomWidth-1)
    innerRoomVertOffset = _random(1, h-innerRoomHeight-1)
    inner_room_key_level = _random(0, max_key_level)
    #first, dig the whole space.
    put_rect_of_tiles(x, y, w, h)
    #place the inner room:
    makeOutline(x+innerRoomHorizOffset, y+innerRoomVertOffset, innerRoomWidth, innerRoomHeight, _WALL_CODE, inner_room_key_level)
    #re-dig inner room. We do that for proper curr_key_level setup for that room.
    put_rect_of_tiles(x+innerRoomHorizOffset+1, y+innerRoomVertOffset+1, innerRoomWidth-2, innerRoomHeight-2, _FLOOR_CODE, inner_room_key_level)
    #place the door for the inner room:
    doorIsOnUpperOrLowerWall = _random(0, 1)
    if doorIsOnUpperOrLowerWall:
        doorX = x + innerRoomHorizOffset + _random(1, innerRoomWidth-2)
        doorY = y + innerRoomVertOffset + _random(0, 1)*(innerRoomHeight - 1)
    else:
        doorY = y + innerRoomVertOffset + _random(1, innerRoomHeight - 2)
        doorX = x + innerRoomHorizOffset + _random(0, 1)*(innerRoomWidth - 1)
    put_single_tile(doorX, doorY, _DOOR_CODE, inner_room_key_level)


def digEllipticRoom(x, y, w, h, entryX, entryY):
    global current_map
    if w < 5 or h < 5:
        return
    roomXRadius = int(w / 2)
    roomYRadius = int(h / 2)
    if w % 2 == 0:
        roomXRadius -= 1
    if h % 2 == 0:
        roomYRadius -= 1
    entryCorrLength = (w if w > h else h)
    roomCenterX = x + roomXRadius
    roomCenterY = y + roomYRadius
    for i in range (x, x+w):
        for j in range (y, y+h):
            currRelativeCoordX = i - roomCenterX
            currRelativeCoordY = j - roomCenterY
            currXComponent = (currRelativeCoordX ** 2) * (roomYRadius ** 2)
            currYComponent = (currRelativeCoordY ** 2) * (roomXRadius ** 2)
            if currXComponent + currYComponent <= (roomXRadius ** 2) * (roomYRadius ** 2):
                put_single_tile(i, j, _FLOOR_CODE)
    digEntryCorridor(x, y, w, h, entryX, entryY, entryCorrLength)


def digCircularOutlinedRoom(x, y, w, h, entryX, entryY): # Square room with wall circle inside.
    global current_map
    # w and h should be equal, odd and greater than 5.
    # make w and h equal
    if w < h:
        h = w
    else:
        w = h
    if w < 5 or h < 5:
        return
    put_rect_of_tiles(x, y, w, h)
    # oddity check
    # if w % 2 != 1:
    #     return
    roomRadius = int(w/2) - 1 # behaviour for the even w/h values may be weird.
    roomCenterX = x+roomRadius+1
    roomCenterY = y+roomRadius+1
    for i in range (x, x+w):
        for j in range (y, y+h):
            currRelativeCoordX = i - roomCenterX
            currRelativeCoordY = j - roomCenterY
            if currRelativeCoordX ** 2 + currRelativeCoordY ** 2 <= roomRadius ** 2 and currRelativeCoordX ** 2 + currRelativeCoordY ** 2 >= (roomRadius-1) ** 2:
                put_single_tile(i, j, _WALL_CODE)
    digEntryCorridor(x, y, w, h, entryX, entryY)


#######
#     #
#  #  #
# ### #
#  #  #
#     #
#######
def digRoomWithCross(x, y, w, h):
    global current_map
    put_rect_of_tiles(x, y, w, h)
    roomMiddleX = x+int(w/2)
    roomMiddleY = y + int(h / 2)
    for i in range(x+1, x+w - 1):
        current_map[i][roomMiddleY] = Tile(_WALL_CODE, curr_key_level)
        if h % 2 == 0:
            current_map[i][roomMiddleY-1] = Tile(_WALL_CODE, curr_key_level)
    for i in range(y+1, y+h - 1):
        current_map[roomMiddleX][i] = Tile(_WALL_CODE, curr_key_level)
        if w % 2 == 0:
            current_map[roomMiddleX-1][i] = Tile(_WALL_CODE, curr_key_level)



#########
# # # # #
#       #
# # # # #
#########
def digLongRoom(x, y, w, h): #need to change the name.
    global current_map
    put_rect_of_tiles(x, y, w, h)
    if w < h:
        for i in range(y+1, y+h-1, 2):
            current_map[x][i] = Tile(_WALL_CODE, curr_key_level)
            current_map[x+w-1][i] = Tile(_WALL_CODE, curr_key_level)
    else:
        for i in range(x+1, x+w-1, 2):
            current_map[i][y] = Tile(_WALL_CODE, curr_key_level)
            current_map[i][y+h-1] = Tile(_WALL_CODE, curr_key_level)


###########
# #   #   #
#   #   # #
###########
def digSnakeRoom(x, y, w, h, entryX, entryY):
    global current_map
    obstacleWidth = 0
    put_rect_of_tiles(x, y, w, h)
    if w < h:
        obstacleWidth = w - 1
        for i in range(y+1, y+h-1, 4):
            put_rect_of_tiles(x, i, obstacleWidth, 1, _WALL_CODE)
            if i+2 < y+h:
                put_rect_of_tiles(x + w - obstacleWidth, i + 2, obstacleWidth, 1, _WALL_CODE)
    else:
        obstacleWidth = h - 1
        for i in range(x+1, x+w-1, 4):
            put_rect_of_tiles(i, y, 1, obstacleWidth, _WALL_CODE)
            if i + 2 < x + w:
                put_rect_of_tiles(i + 2, y + h - obstacleWidth, 1, obstacleWidth, _WALL_CODE)
    digEntryCorridor(x, y, w, h, entryX, entryY, 2)


###########################
## THERE ##################
###########################
def choose_shape_and_dig_room(x, y, w, h, entryX, entryY):  # Subject for changes.
    #roomIsDigged = False
    roomType = _random(0, 3)
    if (w >= 7 and h >= 7):
        if roomType == 0:
            digRoomWithInnerRoom(x, y, w, h)
        elif roomType == 1:
            digEllipticRoom(x, y, w, h, entryX, entryY)
        elif roomType == 2:
            digCircularOutlinedRoom(x, y, w, h, entryX, entryY)
        elif roomType == 3:
            digRoomWithCross(x, y, w, h)
    elif w == 2 or h == 2:
        put_rect_of_tiles(x, y, w, h)
    else:
        if roomType == 1:
            digLongRoom(x, y, w, h)
        elif roomType == 2:
            digSnakeRoom(x, y, w, h, entryX, entryY)
        else: put_rect_of_tiles(x, y, w, h)


def is_wall(x, y, w=1, h=1):
    global current_map
    for i in range (x, x+w):
        for j in range(y, y+h):
            if 0 < i < _MAP_WIDTH-1 and 0 < j < _MAP_HEIGHT-1:
                if current_map[i][j].tile_code != _WALL_CODE:
                    return False
            else:
                return  False
    return True


def pickDirectionForDigging(x, y):
    global current_map
    direction = None
    if x >= _MAP_WIDTH or y >= _MAP_HEIGHT:
        print("!!!Oh noes! Coordinates cheburachnulis at ${0}, ${1}!!!".format(x, y))
        #return _Vector(0, 0)
    if current_map[x][y+1].tile_code == _FLOOR_CODE:
        direction = _Vector(0, -1)
    elif current_map[x-1][y].tile_code == _FLOOR_CODE:
        direction = _Vector(1, 0)
    elif current_map[x][y-1].tile_code == _FLOOR_CODE:
        direction = _Vector(0, 1)
    elif current_map[x+1][y].tile_code == _FLOOR_CODE:
        direction = _Vector(-1, 0)
    else:
        direction = _Vector(0, 0)
    return direction


def corridor_endpoint_is_bad(x, y, offset_x, offset_y):  # used only in the try_add_corridor() routine
    RANDOM_SIFTING_THRESHOLD = 99
    if is_wall(x + offset_x, y+offset_y, 1, 1):
        if _random(0, 100) < RANDOM_SIFTING_THRESHOLD:
            return True
    if count_adjacent_walls(x, y) == 1 or \
            count_adjacent_walls(x, y) == 4 and \
            count_diag_walls(x, y) != 4:
        return True
    return False


def corridor_startpoint_is_bad(x, y):  # used only in the try_add_corridor() routine
    if count_adjacent_walls(x, y) == 1:
        return True


def tryAddCorridor():
    global current_map
    for tries in range (_MAX_CORRIDOR_PLACEMENT_TRIES):
        currCell = _Vector()
        corrLength = _random(_MIN_CORRIDOR_LENGTH, _MAX_CORRIDOR_LENGTH)

        while not is_wall(currCell.x, currCell.y) or count_walls_around(currCell.x, currCell.y) < 2:
            currCell = _Vector()

        digDirection = pickDirectionForDigging(currCell.x, currCell.y)
        dirx = digDirection.x
        diry = digDirection.y
        if dirx == diry == 0:
            continue

        # TODO: add dig up/down restrictions (i.e. there should be more "digged horizontally" corridors than "digged vertically" ones)

        if dirx == 1: # dig right
            start_point_x, start_point_y = currCell.x, currCell.y
            end_point_x, end_point_y = currCell.x + corrLength, currCell.y
            horiz = True
            door_x, door_y = start_point_x, start_point_y
            if corridor_startpoint_is_bad(start_point_x, start_point_y) or corridor_endpoint_is_bad(end_point_x, end_point_y, 1, 0):
                continue

        elif dirx == -1: # dig left
            start_point_x, start_point_y = currCell.x - corrLength, currCell.y
            end_point_x, end_point_y = currCell.x, currCell.y
            horiz = True
            door_x, door_y = end_point_x, end_point_y
            if corridor_startpoint_is_bad(end_point_x, end_point_y) or corridor_endpoint_is_bad(start_point_x, start_point_y, -1, 0):
                continue

        elif diry == 1: # dig down
            start_point_x, start_point_y = currCell.x, currCell.y
            end_point_x, end_point_y = currCell.x, currCell.y + corrLength
            horiz = False
            door_x, door_y = start_point_x, start_point_y
            if corridor_startpoint_is_bad(start_point_x, start_point_y) or corridor_endpoint_is_bad(end_point_x, end_point_y, 0, 1):
                continue

        elif diry == -1: # dig up
            start_point_x, start_point_y = currCell.x, currCell.y - corrLength
            end_point_x, end_point_y = currCell.x, currCell.y
            horiz = False
            door_x, door_y = end_point_x, end_point_y
            if corridor_startpoint_is_bad(end_point_x, end_point_y) or corridor_endpoint_is_bad(start_point_x, start_point_y, 0, -1):
                continue

        if horiz:
            if not is_wall(start_point_x, start_point_y-1, corrLength, 3):
                continue
        else:
            if not is_wall(start_point_x-1, start_point_y, 3, corrLength):
                continue

        key_level_start = get_highest_key_level_around(start_point_x, start_point_y)
        key_level_end = get_highest_key_level_around(end_point_x, end_point_y)
        key_level = max(key_level_start, key_level_end)
        put_rect_of_tiles(start_point_x, start_point_y, end_point_x - start_point_x + 1, end_point_y - start_point_y + 1,  _FLOOR_CODE, key_level)
        # if key_level_start != key_level_end:
        #     put_single_tile(start_point_x, start_point_y, _DOOR_CODE, key_level_start)
        #     put_single_tile(end_point_x, end_point_y, _DOOR_CODE, key_level_end)
        # else:
        put_single_tile(door_x, door_y, _DOOR_CODE, key_level)
        return


def tryAddRoom():
    global current_map
    for tries in range (_MAX_ROOM_PLACEMENT_TRIES):
        currCell = _Vector()
        roomW = _random(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
        roomH = _random(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
        horOffset = _random(0, roomW-1)
        vertOffset = _random(0, roomH-1)
        while not is_wall(currCell.x, currCell.y):
            currCell = _Vector()

        digDirection = pickDirectionForDigging(currCell.x, currCell.y)
        dirx = digDirection.x
        diry = digDirection.y
        if dirx == diry == 0:
            continue
        #TODO: add dig up/down restrictions (i.e. there should be more "digged horizontally" rooms than "digged vertically" ones)
        if dirx == 1: # dig right
            if is_wall(currCell.x, currCell.y-vertOffset-1, roomW+2, roomH+2):
                choose_shape_and_dig_room(currCell.x + 1, currCell.y - vertOffset, roomW, roomH, currCell.x, currCell.y)
                put_single_tile(currCell.x, currCell.y, _DOOR_CODE)
                return
        elif dirx == -1: # dig left
            if is_wall(currCell.x-roomW-1, currCell.y-vertOffset-1, roomW+2, roomH+2):
                choose_shape_and_dig_room(currCell.x - roomW, currCell.y - vertOffset, roomW, roomH, currCell.x, currCell.y)
                put_single_tile(currCell.x, currCell.y, _DOOR_CODE)
                return
        elif diry == 1: # dig down
            if is_wall(currCell.x-horOffset-1, currCell.y, roomW+2, roomH+2):
                choose_shape_and_dig_room(currCell.x - horOffset, currCell.y + 1, roomW, roomH, currCell.x, currCell.y)
                put_single_tile(currCell.x, currCell.y, _DOOR_CODE)
                return
        elif diry == -1: # dig up
            if is_wall(currCell.x-horOffset-1, currCell.y-roomH-1, roomW+2, roomH+2):
                choose_shape_and_dig_room(currCell.x - horOffset, currCell.y - roomH, roomW, roomH, currCell.x, currCell.y)
                put_single_tile(currCell.x, currCell.y, _DOOR_CODE)
                return


def count_walls_around(x, y):
    global current_map
    walls = 0
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            if current_map[i][j].tile_code == _WALL_CODE:
                walls += 1
    return walls


def count_adjacent_walls(x, y):
    global current_map
    walls = 0
    for i in [x-1, x+1]:
        if 0 <= i < _MAP_WIDTH and  0 <= y < _MAP_HEIGHT:
            if current_map[i][y].tile_code == _WALL_CODE:
                walls += 1
    for i in [y-1, y+1]:
        if 0 <= x < _MAP_WIDTH and 0 <= i < _MAP_HEIGHT:
            if current_map[x][i].tile_code == _WALL_CODE:
                walls += 1
    return walls

def count_diag_walls(x, y):
    global current_map
    walls = 0
    for i in [x-1, x+1]:
        for j in [y-1, y+1]:
            if 0 <= i < _MAP_WIDTH and 0 <= j < _MAP_HEIGHT:
                if current_map[i][j].tile_code == _WALL_CODE:
                    walls += 1
    return walls

def get_highest_key_level_around(x, y):
    global current_map
    lvl = 0
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            if 0 <= i < _MAP_WIDTH and 0 <= j < _MAP_HEIGHT:
                if current_map[i][j].key_level > lvl:
                    lvl = current_map[i][j].key_level
    return lvl


def is_neighbouring_with_different_key_levels(x, y):
    global current_map
    lvl = current_map[x-1][y-1].key_level
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            if current_map[i][j].key_level != lvl and current_map[i][j].tile_code != _WALL_CODE:  # Walls doesn't count
                return True
    return False


def try_add_more_doors():
    global current_map
    for x in range (2, _MAP_WIDTH - 2):
        for y in range(2, _MAP_HEIGHT - 2):
            if current_map[x][y].tile_code == _FLOOR_CODE:
                curr_walls = count_walls_around(x, y)
                if curr_walls == 6:
                    chance = 15
                else:
                    chance = 95
                if curr_walls >= 6:
                    # try up
                    if current_map[x][y-2].tile_code == _FLOOR_CODE and current_map[x][y-1].tile_code == _WALL_CODE and _rand(100) < chance:
                        current_map[x][y - 1] = Tile(_DOOR_CODE, get_highest_key_level_around(x, y-1))
                    # down
                    if current_map[x][y+2].tile_code == _FLOOR_CODE and current_map[x][y+1].tile_code == _WALL_CODE and _rand(100) < chance:
                        current_map[x][y + 1] = Tile(_DOOR_CODE, get_highest_key_level_around(x, y+1))
                    # right
                    if current_map[x+2][y].tile_code == _FLOOR_CODE and current_map[x+1][y].tile_code == _WALL_CODE and _rand(100) < chance:
                        current_map[x+1][y] = Tile(_DOOR_CODE, get_highest_key_level_around(x+1, y))
                    # left
                    if current_map[x-2][y].tile_code == _FLOOR_CODE and current_map[x-1][y].tile_code == _WALL_CODE and _rand(100) < chance:
                        current_map[x-1][y] = Tile(_DOOR_CODE, get_highest_key_level_around(x-1, y))


def remove_some_random_doors():
    global current_map
    for x in range (_MAP_WIDTH):
        for y in range(_MAP_HEIGHT):
            if current_map[x][y].tile_code == _DOOR_CODE and _rand(100) < 60 and not is_neighbouring_with_different_key_levels(x, y):
                current_map[x][y] = Tile(_FLOOR_CODE)


def placeInitialRoom():
    global current_map
    roomW = _random(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
    roomH = _random(_MIN_ROOM_SIZE, _MAX_ROOM_SIZE)
    halfRoomW = int(roomW / 2)
    halfRoomH = int(roomH / 2)
    halfMapW = int(_MAP_WIDTH / 2)
    halfMapH = int(_MAP_HEIGHT / 2)
    #pickRoomAnddraw_rect_of_chars(halfMapW - halfRoomW, halfMapH - halfRoomH, roomW, roomH)
    digLongRoom(halfMapW - halfRoomW, halfMapH - halfRoomH, roomW, roomH)


def place_stairs():
    global current_map
    x = y = 0
    while (current_map[x][y].tile_code != _FLOOR_CODE or current_map[x][y].key_level != 0 or count_walls_around(x, y) > 3):
        x = _random(2, _MAP_WIDTH - 2)
        y = _random(2, _MAP_HEIGHT - 2)
    put_single_tile(x, y, _DOWN_STAIRS_CODE, 0)

    attempt = 0
    key_level_to_place_downstair = max_key_level
    while (current_map[x][y].tile_code != _FLOOR_CODE or current_map[x][y].key_level != key_level_to_place_downstair or count_walls_around(x, y) > 3):
        x = _random(2, _MAP_WIDTH - 2)
        y = _random(2, _MAP_HEIGHT - 2)
        attempt += 1
        if attempt > 250:
            key_level_to_place_downstair -= 1
            attempt = 0
    put_single_tile(x, y, _UP_STAIRS_CODE, 2)


def update_doors_key_levels():  # shitty workaround
    global current_map
    for x in range(len(current_map)):
        for y in range(len(current_map[0])):
            if current_map[x][y].tile_code == _DOOR_CODE:
                if is_neighbouring_with_different_key_levels(x, y):
                    current_map[x][y].key_level = get_highest_key_level_around(x, y)
                else:
                    current_map[x][y].key_level = 0


def polish_deadend_corridors():
    def maybe_purge(x, y): #  yep, this is a def inside of a def. WHAT A SHITTY-WITTY CODE, OH MY!
        if current_map[x][y].tile_code == _FLOOR_CODE and count_adjacent_walls(x, y) == 3:
            if count_diag_walls(x, y) == 4:
                if _random(0, 10) < 5:
                    put_single_tile(x, y, _WALL_CODE)
            # elif _random(0, 15) < 1:
            #     put_single_tile(x, y, _WALL_CODE)

    global current_map
    for x in range(0, _MAP_WIDTH):
        for y in range(0, _MAP_HEIGHT):
            maybe_purge(x, y)
    for x in range(_MAP_WIDTH, 0, -1):
        for y in range(0, _MAP_HEIGHT):
            maybe_purge(x, y)
    for x in range(0, _MAP_WIDTH):
        for y in range(_MAP_HEIGHT, 0, -1):
            maybe_purge(x, y)
    for x in range(_MAP_WIDTH, 0, -1):
        for y in range(_MAP_HEIGHT, 0, -1):
            maybe_purge(x, y)


def purge_bad_doors():
    global current_map
    for x in range(0, _MAP_WIDTH):
        for y in range(0, _MAP_HEIGHT):
            if current_map[x][y].tile_code == _DOOR_CODE:
                adj_walls = count_adjacent_walls(x, y)
                if adj_walls != 2:
                    put_single_tile(x, y, _FLOOR_CODE)



### MAIN ROUTINE: ###
def generateDungeon(mapw, maph, max_key_levels=2):
    global _MAP_WIDTH, _MAP_HEIGHT, curr_key_level, max_key_level, current_map
    _MAP_WIDTH = mapw
    _MAP_HEIGHT = maph
    max_key_level = max_key_levels

    # Fill the map with solid walls.
    current_map = [[Tile(_WALL_CODE)] * (_MAP_HEIGHT + 1) for _ in range(_MAP_WIDTH + 1)]
    # reset key level
    curr_key_level = 0
    # Place the random room in center of the map.
    placeInitialRoom()

    currentRoomsCount = 1
    currentCorrsCount = 0
    total_count = 0

    while currentRoomsCount < _MAX_ROOMS_COUNT or currentCorrsCount < _MAX_CORRIDORS_COUNT:
        curr_key_level = int((currentRoomsCount / _MAX_ROOMS_COUNT * 10))
        if 0 <= curr_key_level <= 1:
            curr_key_level = 0
        elif 2 <= curr_key_level <= 4:
            curr_key_level = 1
        elif 5 <= curr_key_level <= 10:
            curr_key_level = 2

        if currentCorrsCount < _MAX_CORRIDORS_COUNT:
            tryAddCorridor()
            currentCorrsCount += 1
        if currentRoomsCount < _MAX_ROOMS_COUNT:
            tryAddRoom()
            currentRoomsCount += 1

        total_count += 1

    # draw_shit(current_map)  # <----- DELETE IT

    try_add_more_doors()

    update_doors_key_levels()
    remove_some_random_doors()

    place_stairs()

    makeOutline(0, 0, _MAP_WIDTH, _MAP_HEIGHT, _WALL_CODE)

    # Time for shitty workarounds:
    polish_deadend_corridors()
    purge_bad_doors()

    return current_map

##################################################################################################
# DELETE EVERYTHING BELOW:

# def draw_shit(current_map):
#     import ConsoleWrapper as CW
#     import time
#
#     _WALL_CODE = chr(177)
#     _FLOOR_CODE = '.'
#     _CLDOOR_CODE = '+'
#     _OPDOOR_CODE = '\\'
#
#
#     tile_names = {
#         'wall': _WALL_CODE,
#         'floor': _FLOOR_CODE,
#         'door': _CLDOOR_CODE,
#         'ustairs' : '>',
#         'dstairs': '<',
#         'debugtile': '#'
#     }
#
#
#     tile_colors = {
#         _WALL_CODE: (128, 128, 128),
#         _FLOOR_CODE: (64, 64, 64),
#         _CLDOOR_CODE: (128, 128, 128),
#         _OPDOOR_CODE: (128, 64, 0)
#     }
#
#     key_levels = {
#         0: (128, 128, 128),
#         1: (0, 128, 0),
#         2: (128, 0, 0),
#         3: (128, 0, 128)
#     }
#
#     for i in range(_MAP_WIDTH):
#         for j in range(_MAP_HEIGHT):
#             tile_char = tile_names[current_map[i][j].tile_code]
#             # CW.setForegroundColor(tile_colors[tile_char])
#             CW.setForegroundColor(key_levels[current_map[i][j].key_level])
#             if current_map[i][j].tile_code == 'debugtile':
#                 CW.setForegroundColor(255, 0, 255)
#             CW.putChar(tile_char, i, j)
#
#     CW.flushConsole()
#     # time.sleep(0.1)

