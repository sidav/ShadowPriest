#import Routines.TdlConsoleWrapper as CW
import math

_lastFromX = _lastFromY = -1
_lastVisibilityTable = [[]]



class xy:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def get_line(fromx, fromy, tox, toy):
    line = []
    deltax = abs(tox - fromx)
    deltay = abs(toy - fromy)
    xmod = 1
    ymod = 1
    if tox < fromx:
        xmod = -1
    if toy < fromy:
        ymod = -1
    error = 0
    if deltax >= deltay:
        y = fromy
        deltaerr = deltay
        for x in range(fromx, tox+xmod, xmod):
            line.append(xy(x, y))
            error = error + deltaerr
            if 2 * error >= deltax:
                y = y + ymod
                error -= deltax
    elif deltay > deltax:
        x = fromx
        deltaerr = deltax
        for y in range(fromy, toy+ymod, ymod):
            line.append(xy(x, y))
            error = error + deltaerr
            if 2 * error >= deltay:
                x = x + xmod
                error -= deltay
    return line

#two-stage LOS check
#returns the visibility map from the view from fromx, fromy coords. True means that the cell is visible, False - not visible.

_visionObstructingMap = [[]] #True if the cell blocks line of sight, False otherwise.

def setvisionObstructingMap(visionObstructingMap):
    global _visionObstructingMap
    _visionObstructingMap = visionObstructingMap

def _straightLOSCheck(fromx, fromy, tox, toy):
    #Checks visible Line of Sight between two tiles
    #Uses straight Brasanham's Line
    #Kinda "first stage check", CAN NOT provide any final result
    mapW = len(_visionObstructingMap)
    mapH = len(_visionObstructingMap[0])
    line = get_line(fromx, fromy, tox, toy)
    lineLength = len(line)

    for i, currCell in enumerate(line):
        x = currCell.x
        y = currCell.y
        if (x < 0 or y < 0 or x > mapW-1 or y > mapH-1):
            return False
        if _visionObstructingMap[x][y] == True and i < lineLength-1:
            return False
    return True

def fullLOSLineCheck(fromx, fromy, viewRange = -1):
    #Very experimental alternate first stage
    #The difference is that this first-stage variant is MUCH faster (approx 20 times faster!)
    #it also has the vision range check.
    #  TODO: add out of bounds check
    mapW = len(_visionObstructingMap)
    mapH = len(_visionObstructingMap[0])
    fullView = [[False] * (mapH) for _ in range(mapW)]
    for bx in range(mapW):
        for by in range(mapH):
            if 0 < bx < mapW-1 and 0 < by < mapH-1:
                continue
            #print ("x{} y{}".format(bx, by))
            line = get_line(fromx, fromy, bx, by)
            lineLength = len(line)
            for i, currCell in enumerate(line):
                x = currCell.x
                y = currCell.y
                if i == 0: # TODO: is the starting cell visible?
                    # TODO: The answer is 'yes' here.
                    fullView[x][y] = True
                    continue
                # if (x < 0 or y < 0 or x > mapW - 1 or y > mapH - 1):
                #     return False
                if (x-fromx)**2 + (y-fromy)**2 > viewRange ** 2 and viewRange != -1:
                    break
                if _visionObstructingMap[x][y] == False and i < lineLength - 1:
                    fullView[x][y] = True
                else:
                    fullView[x][y] = True
                    break
    return fullView

def _checkNeighbouringTiles(x, y, firstStageTable): #checks if the tile has some first-stage-visible neighbours
    mapW = len(firstStageTable)
    mapH = len(firstStageTable[0])
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if not ((0 < x+i < mapW) and (0 < y+j < mapH)):
                continue
            if abs(i*j) == 1:
                continue
            if firstStageTable[x+i][y+j] and not _visionObstructingMap[x+i][y+j]:
                return True
    return False



def getVisibilityTableFromPosition(fromx, fromy, table=None, vision_range=-1):
    if table is not None:
        setvisionObstructingMap(table)
    mapW = len(_visionObstructingMap)
    mapH = len(_visionObstructingMap[0])
    resultingMap = [[False] * mapH for _ in range(mapW)]
    #first stage
    #firstStage = [[False] * (mapH) for _ in range(mapW)]
    # for i in range(mapW):
    #     for j in range(mapH):
    #         firstStage[i][j] = _straightLOSCheck(fromx, fromy, i, j)
    firstStage = fullLOSLineCheck(fromx, fromy, viewRange=vision_range)
    #second stage
    secondStage = [[False] * (mapH) for _ in range(mapW)]
    for i in range(mapW):
        for j in range(mapH):
            if firstStage[i][j]:
                continue
            if _visionObstructingMap[i][j]:
                secondStage[i][j] = _checkNeighbouringTiles(i, j, firstStage)
    #merging stages
    for i in range(mapW):
        for j in range(mapH):
            resultingMap[i][j] = bool(firstStage[i][j] or secondStage[i][j])
    return resultingMap


def is_point_in_sector(from_x, from_y, look_x, look_y, target_x, target_y, sector_angle):
    half_of_sector_angle = (sector_angle / 2) * math.pi / 180
    centered_x, centered_y = target_x - from_x, target_y - from_y
    looking_angle = math.atan2(look_y, look_x)
    taget_angle = math.atan2(centered_y, centered_x)
    if centered_x < 0 and centered_y < 0 and look_y >= 0:
        taget_angle += 2 * math.pi
    if looking_angle - half_of_sector_angle <= taget_angle <= looking_angle + half_of_sector_angle:
        return True
    return False

# def visibleLineExists(fromx, fromy, tox, toy): # TODO: rewrite lol
#     global _lastFromX, _lastFromY, _lastVisibilityTable
#     mapW = len(_visionObstructingMap)
#     mapH = len(_visionObstructingMap[0])
#     if fromx == tox and fromy == toy:
#         return True
#     if fromx < 0 or fromx >= mapW or fromy < 0 or fromy >= mapH:
#         return False
#     if fromx == _lastFromX and fromy == _lastFromY and _lastVisibilityTable != [[]]:
#         try:
#             return bool(_lastVisibilityTable[tox][toy])
#         except:
#             print("PROBLEM: tox = {}, toy = {}".format(tox, toy))
#     else:
#         _lastFromX = fromx
#         _lastFromY = fromy
#         _lastVisibilityTable = getVisibilityTable(fromx, fromy)
#         return bool(_lastVisibilityTable[tox][toy])
