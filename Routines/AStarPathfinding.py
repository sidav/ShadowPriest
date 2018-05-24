#A* pathfinding algorithm


class Cell:

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


STRAIGHT_COST = 10
DIAGONAL_COST = 14
diagonalsAllowed = True
openlist = []
closedlist = []
finalReversedPath = []
cellmap = []
target = None
origin = None


def _abs(t):
    if t < 0:
        return -t
    return t


def _are_coords_valid(x, y):
    if 0 <= x < len(cellmap) and 0 <= y < len(cellmap[0]):
        return True
    return False


def _manhattans_heuristic(fromx, fromy, tox, toy):
    return 10*(_abs(tox - fromx) + _abs(toy - fromy))


def _consider_neighbours(curcell):
    global diagonalsAllowed, openlist, closedlist, finalReversedPath, cellmap, target, origin
    cost = 0
    x = curcell.x
    y = curcell.y
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            if _are_coords_valid(x+i, y+j) and (i != 0 or j != 0):
                if i*j != 0: #if that neighbour lays diagonally...
                    if not diagonalsAllowed:
                        continue
                    else:
                        cost = DIAGONAL_COST
                else:
                    cost = STRAIGHT_COST
                curneighbour = cellmap[x + i][y + j]
                if curneighbour.passable and curneighbour not in closedlist:
                    if curneighbour not in openlist:
                        openlist.append(curneighbour)
                        curneighbour.parent = curcell
                        curneighbour.setG(cost)
                    else: #Here be dragons. I didn't understand that part completely.
                        if curneighbour.g > curcell.g + cost:
                            curneighbour.parent = curcell
                            curneighbour.setG(cost)


def _get_cell_with_lowest_F():
    global diagonalsAllowed, openlist, closedlist, finalReversedPath, cellmap, target, origin
    cheapestcell = openlist[0]
    for i in openlist:
        if i.getF() < cheapestcell.getF():
            cheapestcell = i
    return cheapestcell


def _reverse_path_list(path):
    global target, origin
    final_path = []
    curcell = target
    while curcell != origin:
        final_path.append(curcell)
        curcell = curcell.parent
    return final_path


def _do_pathfinding():
    global diagonalsAllowed, openlist, closedlist, finalReversedPath, cellmap, target, origin
    #some pre-checks:
    if not target.passable:
        print("Target square is non-passable!")
        return []  # finalReversedPath
    #step 1:
    targetReached = False
    openlist.append(origin)
    #step 2:
    while not targetReached:
        #substep 2a:
        currentCell = _get_cell_with_lowest_F()
        #substep 2b:
        closedlist.append(currentCell)
        openlist.remove(currentCell)
        #substep 2c:
        _consider_neighbours(currentCell)
        # substep 2d:
        if target in openlist:
            #step 3:
            targetReached = True
            finalReversedPath = _reverse_path_list(finalReversedPath)
        if len(openlist) == 0 and not targetReached:
            print("No path exists!")
            break
    return finalReversedPath


def get_path_cost():
    global diagonalsAllowed, openlist, closedlist, finalReversedPath, cellmap, target, origin
    if len(finalReversedPath) > 0:
        return finalReversedPath[0].g
    else:
        return -1  # error or something


def get_path(inpboolmap, fromx, fromy, tox, toy, allowDiags = True):
    _init_values(inpboolmap, fromx, fromy, tox, toy, allowDiags)
    return _do_pathfinding()


def get_next_step_to_target(inpboolmap, fromx, fromy, tox, toy, allowDiags = True):
    _init_values(inpboolmap, fromx, fromy, tox, toy, allowDiags)
    path = _do_pathfinding()
    if len(path) == 0:
        return 0, 0
    next_cell_in_path = path[-1]
    next_x = next_cell_in_path.x - origin.x
    next_y = next_cell_in_path.y - origin.y
    return next_x, next_y


def _init_values(inpboolmap, fromx, fromy, tox, toy, allowDiags = True):
    global diagonalsAllowed, openlist, closedlist, finalReversedPath, cellmap, target, origin
    diagonalsAllowed = allowDiags
    x = len(inpboolmap)
    y = len(inpboolmap[0])
    openlist = []
    closedlist = []
    finalReversedPath = []
    cellmap = [[0] * y for _ in range(x)]
    for i in range(x):
        for j in range(y):
            cellmap[i][j] = Cell(i, j, inpboolmap[i][j], h=_manhattans_heuristic(i, j, tox, toy))
    target = cellmap[tox][toy]
    origin = cellmap[fromx][fromy]

# def __init__(self, inpboolmap, fromx, fromy, tox, toy, allowDiags = True):
#     self.diagonalsAllowed = allowDiags
#     x = len(inpboolmap)
#     y = len(inpboolmap[0])
#     self.openlist = []
#     self.closedlist = []
#     self.finalReversedPath = []
#     self.cellmap = [[0] * y for _ in range(x)]
#     for i in range(x):
#         for j in range(y):
#             self.cellmap[i][j] = cell(i, j, inpboolmap[i][j], h=self._manhattans_heuristic(i, j, tox, toy))
#     self.target = self.cellmap[tox][toy]
#     self.origin = self.cellmap[fromx][fromy]
    #self.currentCell = self.origin


#АЛГОРИТМ А*:
        #Замечание: F = G+H, где G - цена пути ИЗ стартовой точки, H - эвристическая оценка пути ДО цели.
        #По "методу Манхэттена": H = 10 * (_abs(targetX - startX) + _abs(targetY-startY))
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