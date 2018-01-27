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

_MIN_SPLIT_FACTOR = 40 #In percent
_MAX_SPLIT_FACTOR = 100 - _MIN_SPLIT_FACTOR #In percent
_MIN_ROOM_WIDTH = 3
_MIN_ROOM_HEIGHT = 3
_SPLITS = 12

_FLOOR_CODE = 'floor'
_WALL_CODE = 'wall'
_DOOR_CODE = 'door'

class treeNode:
    def __init__(self, parent=None, cont=None):
        self.parent = parent
        self.left = None
        self.right = None
        self.cont = cont

    def get_leafs_of_level(self, lvl, nodelist=None): #should be called from the root node only
        if nodelist == None:
            nodelist = []
        if lvl == 0:
            nodelist.append(self)
        else:
            if self.left is not None:
                self.left.get_leafs_of_level(lvl - 1, nodelist)
            if self.right is not None:
                self.right.get_leafs_of_level(lvl - 1, nodelist)
        return nodelist

    def getLeafs(self, leafs=None):
        if leafs == None:
            leafs = []
        if self.left is None and self.right is None:
            leafs.append(self)
        if self.left is not None:
            self.left.getLeafs(leafs)
        if self.right is not None:
            self.right.getLeafs(leafs)
        return leafs

    def splitSelf(self): #BSP splitting
        selfx = self.cont.x
        selfy = self.cont.y
        selfw = self.cont.w
        selfh = self.cont.h
        horiz = _random(0, 1)  # 1 is horizontal splitting, 0 is vertical
        for _ in range(5): #5 is just a number of tries
            horizOK = True
            vertOK = True
            factor = _random(_MIN_SPLIT_FACTOR, _MAX_SPLIT_FACTOR)
            lefthorizh = selfh*factor//100
            righthorizh = selfh - lefthorizh
            leftvertw = selfw*factor//100
            rightvertw = selfw - leftvertw
            if (lefthorizh < _MIN_ROOM_HEIGHT or righthorizh < _MIN_ROOM_HEIGHT):
                horiz = 0
                horizOK = False
            if (leftvertw < _MIN_ROOM_WIDTH or rightvertw < _MIN_ROOM_WIDTH):
                vertOK = False
                continue
        if not (horizOK and vertOK):
            return
        if horiz == 1: #horizontal split
            leftc = Container(selfx, selfy, selfw, lefthorizh, "LHORIZONTAL")
            rightc = Container(selfx, selfy+lefthorizh, selfw, righthorizh, "RHORIZONTAL")
            self.left = treeNode(self, leftc)
            self.right = treeNode(self, rightc)
        else: #vertical split
            leftc = Container(selfx, selfy, leftvertw, selfh, "LVERTICAL")
            rightc = Container(selfx+leftvertw, selfy, rightvertw, selfh, "RVERTICAL")
            self.left = treeNode(self, leftc)
            self.right = treeNode(self, rightc)


class Container:
    def __init__(self, x, y, w, h, vh = "UNDEF"):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vh = vh

    def addToMap(self, arr):
        x0 = self.x-1
        y0 = self.y-1
        h = self.h+1
        w = self.w+1
        for i in range(x0, x0 + w):
            arr[i][y0] = _WALL_CODE
            try:
                arr[i][y0+h-1] = _WALL_CODE
            except:
                print("BSP SECTOR PLACEMENT ERROR AT  x {}, y {}".format(i, y0+h-1))
        for j in range(y0, y0 + h):
            arr[x0][j] = _WALL_CODE
            try:
                arr[x0+w-1][j] = _WALL_CODE
            except:
                print("BSP SECTOR PLACEMENT ERROR AT x {}, y {}".format(i, y0+h-1))
#############################################################################################################
#############################################################################################################
def splitNTimes(root, N):
    for _ in range(N):
        leafs = root.getLeafs()
        for l in leafs:
            l.splitSelf()

def placeConnections(root, arr):
    # the following loop will draw the connections between the nodes with the same parent.
    # It creates smth like doorways or even removes some walls.
    # I'm glad of the result. Really.
    traverseEnded = False
    curlvl = 0
    while not traverseEnded:
        a = root.get_leafs_of_level(curlvl)
        if len(a) is 0:
            traverseEnded = True
        for i in a:
            if i.left is not None and i.right is not None:
                fx = i.left.cont.x + i.left.cont.w // 2
                fy = i.left.cont.y + i.left.cont.h // 2
                tx = i.right.cont.x + i.right.cont.w // 2
                ty = i.right.cont.y + i.right.cont.h // 2
                if fx == tx:
                    for k in range(fy, ty + 1):
                        arr[fx][k] = _FLOOR_CODE
                elif fy == ty:
                    for k in range(fx, tx + 1):
                        arr[k][fy] = _FLOOR_CODE
        curlvl += 1

def placeDoors(arr):
    for i in range(1, len(arr)-1):
        for j in range(1, len(arr[0])-1):
            #horizontal doors:
            if arr[i][j] == _FLOOR_CODE and arr[i][j-1] == _WALL_CODE and arr[i][j+1] == _WALL_CODE and arr[i-1][j] == _FLOOR_CODE and arr[i+1][j] == _FLOOR_CODE \
                    and (arr[i-1][j - 1] == _FLOOR_CODE or arr[i+1][j - 1] == _FLOOR_CODE or arr[i-1][j + 1] == _FLOOR_CODE or arr[i+1][j + 1] == _FLOOR_CODE  ):
                arr[i][j] = _DOOR_CODE
            #vertical doors:
            elif arr[i][j] == _FLOOR_CODE and arr[i-1][j] == _WALL_CODE and arr[i+1][j] == _WALL_CODE and arr[i][j-1] == _FLOOR_CODE and arr[i][j+1] == _FLOOR_CODE \
                    and (arr[i - 1][j - 1] == _FLOOR_CODE or arr[i + 1][j - 1] == _FLOOR_CODE or arr[i - 1][j + 1] == _FLOOR_CODE or arr[i + 1][j + 1] == _FLOOR_CODE):
                arr[i][j] = _DOOR_CODE


def makeWallOutline(arr): #just to be sure that the map won't be open to its borders.
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            if i == 0 or j == 0 or i == len(arr)-1 or j == len(arr[0])-1:
                arr[i][j] = _WALL_CODE

def setTileCodes(floor, wall, door):
    global _FLOOR_CODE, _WALL_CODE, _DOOR_CODE
    _FLOOR_CODE = floor
    _WALL_CODE = wall
    _DOOR_CODE = door

def __generateMap(mapW, mapH):
    outp = [[_FLOOR_CODE] * (mapH) for _ in range(mapW)]
    con = Container(1, 1, mapW-1, mapH-1)
    BSPRoot = treeNode(cont = con)
    splitNTimes(BSPRoot, _SPLITS)
    leafs = BSPRoot.getLeafs()
    for i in leafs:
        i.cont.addToMap(outp)
    placeConnections(BSPRoot, outp)
    placeDoors(outp)
    #makeWallOutline(outp) <-- No need now!
    return outp


def generateMapWithRandomParams(mapW, mapH, seed = -1): #this may cause crap
    global _MIN_SPLIT_FACTOR, _MAX_SPLIT_FACTOR, _MIN_ROOM_WIDTH, _MIN_ROOM_HEIGHT, _SPLITS

    if seed != -1:
        setRandomSeed(seed)

    _MIN_SPLIT_FACTOR = _random(20, 50)
    _MAX_SPLIT_FACTOR = 100 - _MIN_SPLIT_FACTOR
    _MIN_ROOM_WIDTH = _random(2, 4)
    _MIN_ROOM_HEIGHT = _random(2, 5)
    _SPLITS = _random(2,25)

    return __generateMap(mapW, mapH)


def generateMapWithGivenParams(mapW, mapH, minSplitFactor = 40, minRoomWidth = 3, minRoomHeight = 3, splits = 12, seed = -1): #this will not cause crap most of the time
    global _MIN_SPLIT_FACTOR, _MAX_SPLIT_FACTOR, _MIN_ROOM_WIDTH, _MIN_ROOM_HEIGHT, _SPLITS

    if seed != -1:
        setRandomSeed(seed)

    _MIN_SPLIT_FACTOR = minSplitFactor  # In percent
    _MAX_SPLIT_FACTOR = 100 - _MIN_SPLIT_FACTOR  # In percent
    _MIN_ROOM_WIDTH = minRoomWidth
    _MIN_ROOM_HEIGHT = minRoomHeight
    _SPLITS = splits

    return __generateMap(mapW, mapH)

