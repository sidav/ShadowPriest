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
        _LCG_X = 7355608                                                    #
    LCG_A = 14741                                                           #
    LCG_C = 757                                                             #
    LCG_M = 77777677777                                                     #
    _LCG_X = (LCG_A*_LCG_X + LCG_C) % LCG_M                                 #
    return _LCG_X%mod                                                       #
#############################################################################

def randHorDir(): #What a shame.
    return _random(-1, 1)

def randVertDir(): #What a shame.
    val = _random(0, 100)
    if val < 30:
        return -1
    elif val > 70:
        return 1
    else:
        return 0


TOTAL_LAND_AUTOMS = 8
TOTAL_MNT_AUTOMS = 5
TOTAL_FOREST_AUTOMS = 12
TOTAL_FIELD_AUTOMS = 5
LAND_CYCLES = 620
MNT_CYCLES = 175
FOREST_CYCLES = 50
FIELD_CYCLES = 15
#_SINGLE_ELEMENT_PLACEMENT_TRIES = 10000
_WATER_CODE = '~'
_GROUND_CODE = '.'
_MOUNTAIN_CODE = '^'
_FOREST_CODE = 'f'
_FIELD_CODE = '"'
_TOWN_CODE = 'O'
_MILITARY_BASE_CODE = '%'
_LAB_CODE = '&'

class Automata:
    def __init__(self, x, y, maparr, brush, allowed = []):
        self.x = x
        self.y = y
        self.maparr = maparr
        self.brush = brush
        self.allowed = allowed
        self.allowed.append(self.brush)

    def step(self):
        MAX_DIRECTION_TRIES = 1000
        dx = randHorDir()
        dy = randVertDir()
        for _ in range(MAX_DIRECTION_TRIES):
            while dx*dy != 0 or dx == dy:
#                randomize()
                dx = randHorDir()
                dy = randVertDir()
            if (0 < self.x+dx < len(self.maparr)-2 and 0 < self.y+dy < len(self.maparr[0])-2) and self.maparr[self.x+dx][self.y+dy] in self.allowed:
                self.x += dx
                self.y += dy
                self.maparr[self.x][self.y] = self.brush
                break

def addLandscapeElements(maparr, automs, brush, allowed:list, cycles, randomPlacement = True, minDistanceToMapBorder = 15):
    mapW = len(maparr)
    mapH = len(maparr[0])
    auts = []
    if randomPlacement:
        for i in range(1, automs + 1):
            selx = _random(0+minDistanceToMapBorder, mapW-minDistanceToMapBorder)
            sely = _random(0+minDistanceToMapBorder, mapH-minDistanceToMapBorder)
            while maparr[selx][sely] not in allowed:
                selx = _random(0 + minDistanceToMapBorder, mapW - minDistanceToMapBorder)
                sely = _random(0 + minDistanceToMapBorder, mapH - minDistanceToMapBorder)
            auts.append(Automata(selx, sely, maparr, brush, allowed))
    else:
        for i in range(1, automs+1):
            x = i * mapW // (TOTAL_LAND_AUTOMS + 1)
            y = i * mapH // (TOTAL_LAND_AUTOMS + 1)
            auts.append(Automata(x, y, maparr, _GROUND_CODE, [_WATER_CODE]))
    for aut in auts:
        for _ in range(cycles):
            aut.step()


def countSurroundings(maparr, x, y, code): #returns the number of given surroundings for the tile
    mapW = len(maparr)
    mapH = len(maparr[0])
    result = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if not (0 < x+i < mapW and 0 < y+j < mapH):
                continue
            if (i !=0 or j != 0) and maparr[x+i][y+j] == code:
                result += 1
    return result


#Crap, but working
def tryRandomlyAddSingleElements(maparr, elemCode, neighbours:list, neighborMinNumber:list, elemCount:int, minDistance = 2):
    _SINGLE_ELEMENT_PLACEMENT_TRIES = 500
    #adds some single-tile element (i.e. town, military base...) on the random map
    mapW = len(maparr)
    mapH = len(maparr[0])
    x = 0
    y = 0
    placedXcoords = [0] * (elemCount+1) #coords of already placed elems
    placedYcoords = [0] * (elemCount+1) #coords of already placed elems
    totalPlaced = 0

    for currentPlacingElementNumber in range(elemCount+1):
        for _ in range(_SINGLE_ELEMENT_PLACEMENT_TRIES):
            successfulPlacement = True
            distanceSatisfied = False
            #The following loop is the distance check.
            #Elems should not be placed closer than minDistance allows
            while not distanceSatisfied and currentPlacingElementNumber > 0:
                x = _random(1, mapW - 1)
                y = _random(1, mapH - 1)
                for i in range(currentPlacingElementNumber):
                    if (x-placedXcoords[i]) ** 2 + (y - placedYcoords[i]) ** 2 < minDistance ** 2:
                        distanceSatisfied = False
                        break
                    else:
                        distanceSatisfied = True
            #Checking necessary neighbours condition.
            for i, currentCheck in enumerate(neighbours):
                currentCheckCount = countSurroundings(maparr, x, y, currentCheck)
                if currentCheckCount < neighborMinNumber[i] :
                    successfulPlacement = False
                    break
            if not successfulPlacement:
                continue
            #place elems, add placed coords to the array.
            maparr[x][y] = elemCode
            if (currentPlacingElementNumber != elemCount):
                placedXcoords[currentPlacingElementNumber] = x
                placedYcoords[currentPlacingElementNumber] = y
            totalPlaced += 1
            break
    if totalPlaced < elemCount:
        return False
    return True

#TODO: add the possibility to choose unnecessary neighbours (like "mountain OR forest")
#TODO: SPEED THE FUCK UP THIS CRAP!
def tryAddSingleElements(maparr, elemCode, neighbours:list, neighborMinNumber:list, elemCount:int, minDistance = 2):
    #adds some single-tile element (i.e. town, military base...) on the random map
    mapW = len(maparr)
    mapH = len(maparr[0])
    x = 1
    y = 1
    placedXcoords = [0] * elemCount #coords of already placed elems
    placedYcoords = [0] * elemCount #coords of already placed elems
    totalPlaced = 0
    for currentPlacingElementNumber in range(elemCount):
        #for _ in range(_SINGLE_ELEMENT_PLACEMENT_TRIES): # <-- not needed if placement coords aren't random...
        distanceSatisfied = False
        while True:
            successfulPlacement = True
            x += 1#random(1, mapW - 1)
            #y = _random(1, mapH - 1)
            if x >= mapW:
                x = 0
                y+=1
            if  (y == mapH):
                return False
            if maparr[x][y] == _WATER_CODE:
                continue
            #check distance satisfaction...
            if currentPlacingElementNumber > 0:
                for i in range(currentPlacingElementNumber):
                    currSquareDist = (x-placedXcoords[i]) ** 2 + (y - placedYcoords[i]) ** 2
                    distanceSatisfied = currSquareDist >= minDistance ** 2
                    if not distanceSatisfied:
                        break
                if not distanceSatisfied:
                    x += currSquareDist//4
                    continue
            #Checking necessary neighbouring tiles condition.
            for i, currentCheck in enumerate(neighbours):
                currentCheckCount = countSurroundings(maparr, x, y, currentCheck)
                if currentCheckCount < neighborMinNumber[i] :
                    successfulPlacement = False
                    break
            if not successfulPlacement:
                continue
            #place elems, add placed coords to the arrays.
            maparr[x][y] = elemCode
            if (currentPlacingElementNumber != elemCount):
                placedXcoords[currentPlacingElementNumber] = x
                placedYcoords[currentPlacingElementNumber] = y
            totalPlaced += 1
            break
    if totalPlaced < elemCount:
        return False
    return True


# def drawMap(maparr):
#     for i in range(len(maparr)):
#         for j in range(len(maparr[i])):
#             if maparr[i][j] == _WATER_CODE:
#                 setForegroundColor(0, 64, 255)
#             elif maparr[i][j] == _GROUND_CODE:
#                 setForegroundColor(200, 64, 64)
#             elif maparr[i][j] == _MOUNTAIN_CODE:
#                 setForegroundColor(200, 200, 200)
#             elif maparr[i][j] == _FOREST_CODE:
#                 setForegroundColor(0, 255, 64)
#             elif maparr[i][j] == _FIELD_CODE:
#                 setForegroundColor(220, 220, 0)
#             elif maparr[i][j] == _TOWN_CODE:
#                 setForegroundColor(255, 128, 255)
#             elif maparr[i][j] == _MILITARY_BASE_CODE:
#                 setForegroundColor(255, 0, 0)
#             elif maparr[i][j] == _LAB_CODE:
#                 setForegroundColor(0, 255, 255)
#             putChar(maparr[i][j], i, j)

def generateMap(mapW, mapH):
    while True:
        maparr = [[_WATER_CODE] * (mapH) for _ in range(mapW)]
        #land
        addLandscapeElements(maparr, TOTAL_LAND_AUTOMS, _GROUND_CODE, [_WATER_CODE], LAND_CYCLES, False, minDistanceToMapBorder=8)
        #mountains
        addLandscapeElements(maparr, TOTAL_MNT_AUTOMS, _MOUNTAIN_CODE, [_GROUND_CODE], MNT_CYCLES,
                             minDistanceToMapBorder=4)
        # forest
        addLandscapeElements(maparr, TOTAL_FOREST_AUTOMS, _FOREST_CODE, [_GROUND_CODE, _MOUNTAIN_CODE], FOREST_CYCLES,
                             minDistanceToMapBorder=4)
        #fields
        addLandscapeElements(maparr, TOTAL_FIELD_AUTOMS, _FIELD_CODE, [_GROUND_CODE, _FOREST_CODE], FIELD_CYCLES,
                             minDistanceToMapBorder=2)
        # towns
        Neigh = [_FIELD_CODE]
        NeighNum = [3]
        if not tryAddSingleElements(maparr, _TOWN_CODE, Neigh, NeighNum, elemCount=TOTAL_FIELD_AUTOMS, minDistance=7):
            continue
        # Military
        Neigh = [_GROUND_CODE]
        NeighNum = [7]
        if not tryAddSingleElements(maparr, _MILITARY_BASE_CODE, Neigh, NeighNum, 2, minDistance=15):
            continue
        # Labs
        Neigh = [_MOUNTAIN_CODE]
        NeighNum = [7]
        if not tryAddSingleElements(maparr, _LAB_CODE, Neigh, NeighNum, 2, minDistance=7):
            continue
        break
    return maparr
