#There I'll try to implement "Simple pathfinding for a dungeon" by Pieter Droogendijk.
#It should be simple as crap, but it isn't.
#It is almost finished (it works at least), but it needs some cosmetic work.
class cell:
    def __init__(self, x, y, passabru, value):
        self.x = x
        self.y = y
        self.passable = passabru
        self.value = value

class cellStack:

    def __init__(self):
        self.stack = []

    def push(self, crap):
        self.stack.append(crap)

    def pop(self):
        if len(self.stack) == 0:
            print("pop is fucked up.")
            return None
        ret = self.stack[len(self.stack)-1]
        self.stack.remove(ret)
        return ret

    def shift(self):
        if len(self.stack) == 0:
            print("shift is fucked up.")
            return None
        ret = self.stack[0]
        self.stack.remove(ret)
        return ret

class CrapPathfinding:

    def abs(self, t):
        if t < 0:
            return -t
        return t

    def coordsValid(self, x, y):
        if 0 <= x < len(self.boolmap) and 0 <= y < len(self.boolmap[0]):
            return True
        return False

    def selectNextInPath(self):
        x = self.currentCell.x
        y = self.currentCell.y
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if self.coordsValid(x+i, y+j) and (i != 0 or j != 0):
                    if self.cellmap[x+i][y+j].passable and self.cellmap[x+i][y+j].value == self.currentCell.value-1:
                        selectedSquare = self.cellmap[x+i][y+j] #yep, we have selected that one.
                        return selectedSquare
        return None #There isn't any adjacent squares which value is by 1 less than needed.

    def selectAdjacentZeroValueSquare(self):
        x = self.currentCell.x
        y = self.currentCell.y
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if self.coordsValid(x+i, y+j) and (i != 0 or j != 0) and (self.diagonalsAllowed or abs(i) + abs(j) != 2):
                    if self.cellmap[x+i][y+j].value == 0 and self.cellmap[x+i][y+j].passable and self.cellmap[x+i][y+j] != self.origin:
                        selectedSquare = self.cellmap[x+i][y+j] #yep, we have selected that one.
                        selectedSquare.value = self.currentCell.value + 1
                        return selectedSquare
        return None #There isn't any adjacent squares with zero value

    def findPath(self):
        #some pre-checks:
        if not self.target.passable:
            print("Target square is non-passable!")
            return self.finalReversedPath
        #step 1 is missing (it is in the constructor)
        goto7 = False
        #next loop is from step 6
        while not goto7:
            #steps 2-4
            while True:
                selectedSquare = self.selectAdjacentZeroValueSquare()
                if selectedSquare is None:
                    break
                if selectedSquare == self.target:
                    self.currentCell = selectedSquare
                    goto7 = True
                    break
                self.unfinished.push(selectedSquare)
            if (goto7):
                break
            #step 5
            self.currentCell = self.unfinished.shift()
            if self.currentCell == None:
                print("No way exists!")
                return self.finalReversedPath
            #step 6 is "virtual": it's just "goto step 2", so no code there.
        #Step 7 should be virtually done now, i fear. Target is now the current square.
        #steps 8-11:
        while True:
            selectedSquare = self.selectNextInPath()
            self.finalReversedPath.append(self.currentCell)
            self.currentCell = selectedSquare
            if self.currentCell == self.origin:
                self.finalReversedPath.append(self.currentCell)
                break
        return self.finalReversedPath



    def __init__(self, inpboolmap, fromx, fromy, tox, toy, allowDiags = True):
        self.diagonalsAllowed = allowDiags
        x = len(inpboolmap)
        y = len(inpboolmap[0])
        self.boolmap = inpboolmap #if true, then the given cell is passabru!
        self.unfinished = cellStack()
        self.finalReversedPath = []
        self.cellmap = [[0] * y for _ in range(x)]
        for i in range(x):
            for j in range(y):
                self.cellmap[i][j] = cell(i, j, self.boolmap[i][j], 0)
        self.target = self.cellmap[tox][toy]
        self.origin = self.cellmap[fromx][fromy]
        self.currentCell = self.origin

#ORIGINAL TEXT:
# What follows is a way one could implement this algorithm. A 'square' is a
# coordinate on the map. This implementation will use the dungeon map, and a
# stack.
# In a stack, 'push' is to push a value to the top, 'pop' is to pop the value
# last pushed off the stack, and 'shift' is to shift the value first pushed
# (reverse pop).

# 1: Origin is now the current square.
# 2: select an adjacent square who's still set to 0.
   # if there's none, goto 5.
# 3: give the selected square a value of the current square +1.
   # if the selected square is the target, goto 7
# 4: push selected square onto a list of unfinished squares. goto 2.
# 5: shift the first value from the unfinished list, make it the current square.
# 6: goto 2.
# 7: Target is now the current square.
# 8: select an adjacent square.
# 9: if selected square's value is current square -1, set it to the current square.
   # if it's not, goto 8.
# 10:store the position of the current square relative to the selected square
   # (Nort, East, South, West etc.)
   # if it's the origin, goto 12 after that.
# 11:goto 8.
# 12:return list of directions