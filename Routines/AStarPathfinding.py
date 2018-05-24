#A* pathfinding algorithm


class cell:

    def getF(self):
        return self.g + self.h

    def __init__(self, x, y, passabru, parent = None, g = 0, h = 0):
        self.x = x
        self.y = y
        self.passable = passabru
        self.parent = parent
        self.g = g
        self.h = h

    def setG(self, inc):
        if self.parent is not None:
            self.g = self.parent.g + inc


class AStarPathfinding:

    STRAIGHT_COST = 10
    DIAGONAL_COST = 14

    def abs(self, t):
        if t < 0:
            return -t
        return t

    def coordsValid(self, x, y):
        if 0 <= x < len(self.cellmap) and 0 <= y < len(self.cellmap[0]):
            return True
        return False

    def manhattanHeuristic(self, fromx, fromy, tox, toy):
        return 10*(self.abs(tox - fromx) + self.abs(toy - fromy))

    def doNeighbours(self, curcell):
        cost = 0
        x = curcell.x
        y = curcell.y
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if self.coordsValid(x+i, y+j) and (i != 0 or j != 0):
                    if i*j != 0: #if that neighbour lays diagonally...
                        if not self.diagonalsAllowed:
                            continue
                        else:
                            cost = self.DIAGONAL_COST
                    else:
                        cost = self.STRAIGHT_COST
                    curneighbour = self.cellmap[x + i][y + j]
                    if curneighbour.passable and curneighbour not in self.closedlist:
                        if curneighbour not in self.openlist:
                            self.openlist.append(curneighbour)
                            curneighbour.parent = curcell
                            curneighbour.setG(cost)
                        else: #Here be dragons. I didn't understand that part completely.
                            if curneighbour.g > curcell.g + cost:
                                curneighbour.parent = curcell
                                curneighbour.setG(cost)

    def getLowestFCell(self):
        cheapestcell = self.openlist[0]
        for i in self.openlist:
            if i.getF() < cheapestcell.getF():
                cheapestcell = i
        return cheapestcell

    def makePath(self):
        curcell = self.target
        while curcell != self.origin:
            self.finalReversedPath.append(curcell)
            curcell = curcell.parent
        pass


    def findPath(self):
        #some pre-checks:
        if not self.target.passable:
            print("Target square is non-passable!")
            return self.finalReversedPath
        #step 1:
        targetReached = False
        self.openlist.append(self.origin)
        #step 2:
        while not targetReached:
            #substep 2a:
            currentCell = self.getLowestFCell()
            #substep 2b:
            self.closedlist.append(currentCell)
            self.openlist.remove(currentCell)
            #substep 2c:
            self.doNeighbours(currentCell)
            # substep 2d:
            if len(self.openlist) == 0:
                print("No path exists!")
                break
            if self.target in self.openlist:
                #step 3:
                self.makePath()
        return self.finalReversedPath

    def getPathCost(self):
        if len(self.finalReversedPath) > 0:
            return self.finalReversedPath[0].g
        else:
            return -1  # error or something


    def __init__(self, inpboolmap, fromx, fromy, tox, toy, allowDiags = True):
        self.diagonalsAllowed = allowDiags
        x = len(inpboolmap)
        y = len(inpboolmap[0])
        self.openlist = []
        self.closedlist = []
        self.finalReversedPath = []
        self.cellmap = [[0] * y for _ in range(x)]
        for i in range(x):
            for j in range(y):
                self.cellmap[i][j] = cell(i, j, inpboolmap[i][j], h=self.manhattanHeuristic(i, j, tox, toy))
        self.target = self.cellmap[tox][toy]
        self.origin = self.cellmap[fromx][fromy]
        #self.currentCell = self.origin


#АЛГОРИТМ А*:
        #Замечание: F = G+H, где G - цена пути ИЗ стартовой точки, H - эвристическая оценка пути ДО цели.
        #По "методу Манхэттена": H = 10 * (abs(targetX - startX) + abs(targetY-startY))
# 1) Добавляем стартовую клетку в открытый список.
# 2) Повторяем следующее:
    # a) Ищем в открытом списке клетку с наименьшей стоимостью F. Делаем ее текущей клеткой.
    # b) Помещаем ее в закрытый список. (И удаляем с открытого)
    # c) Для каждой из соседних 8-ми клеток ...
        # Если клетка непроходимая или она находится в закрытом списке, игнорируем ее. В противном случае делаем следующее.
        # Если клетка еще не в открытом списке, то добавляем ее туда. Делаем текущую клетку родительской для это клетки. Расчитываем стоимости F, G и H клетки.
        # Если клетка уже в открытом списке, то проверяем, не дешевле ли будет путь через эту клетку. Для сравнения используем стоимость G.
            # Более низкая стоимость G указывает на то, что путь будет дешевле. Эсли это так, то меняем родителя клетки на текущую клетку и пересчитываем для нее стоимости G и F. Если вы сортируете открытый список по стоимости F, то вам надо отсортировать свесь список в соответствии с изменениями.
    # d) Останавливаемся если:
        # Добавили целевую клетку в открытый список, в этом случае путь найден.
        # Или открытый список пуст и мы не дошли до целевой клетки. В этом случае путь отсутствует.
# 3) Сохраняем путь. Двигаясь назад от целевой точки, проходя от каждой точки к ее родителю до тех пор, пока не дойдем до стартовой точки. Это и будет наш путь.