from SidavRandom import * #Can be deleted if the following wrapper will be handled
from ConsoleWrapper import drawCharArray, setForegroundColor, putChar


def random(min, max): #IT'S JUST A WRAPPER. Min, max inclusive!
    return rand(max-min+1)+min

def randHorDir(): #What a shame.
    return random(-1, 1)

def randVertDir(): #What a shame.
    val = random(0, 100)
    if val < 30:
        return -1
    elif val > 70:
        return 1
    else:
        return 0


MAP_WIDTH = 160#80
MAP_HEIGHT = 75#25
TOTAL_LAND_AUTOMS = 26#8
TOTAL_MNT_AUTOMS = 20#5
TOTAL_FOREST_AUTOMS = 14#12
LAND_CYCLES = 1000
MNT_CYCLES = 250
FOREST_CYCLES = 350

class Automata:
    def __init__(self, x, y, maparr, brush, allowed = []):
        self.x = x
        self.y = y
        self.maparr = maparr
        self.brush = brush
        self.allowed = allowed
        self.allowed.append(self.brush)

    def step(self):
        dx = randHorDir()
        dy = randVertDir()
        for _ in range(1000):
            while dx*dy != 0 or dx == dy:
                randomize()
                dx = randHorDir()
                dy = randVertDir()
            if (0 < self.x+dx < len(self.maparr)-2 and 0 < self.y+dy < len(self.maparr[0])-2) and self.maparr[self.x+dx][self.y+dy] in self.allowed:
                self.x += dx
                self.y += dy
                self.maparr[self.x][self.y] = self.brush
                break

def addLandscapeElements(maparr, automs, brush, allowed:list, cycles, randomPlacement = True):
    auts = []
    if randomPlacement:
        for i in range(1, automs + 1):
            selx = random(0, MAP_WIDTH-1)
            sely = random(0, MAP_HEIGHT-1)
            while maparr[selx][sely] not in allowed:
                selx = random(0, MAP_WIDTH - 1)
                sely = random(0, MAP_HEIGHT - 1)
            auts.append(Automata(selx, sely, maparr, brush, allowed))
    else:
        for i in range(1, automs+1):
            x = i * MAP_WIDTH // (TOTAL_LAND_AUTOMS + 1)
            y = i * MAP_HEIGHT // (TOTAL_LAND_AUTOMS + 1)
            auts.append(Automata(x, y, maparr, ".", ["~"]))
    for aut in auts:
        for _ in range(cycles):
            aut.step()

def drawMap(maparr):
    for i in range(len(maparr)):
        for j in range(len(maparr[i])):
            if maparr[i][j] == "~":
                setForegroundColor(0, 64, 255)
            if maparr[i][j] == ".":
                setForegroundColor(200, 64, 64)
            if maparr[i][j] == "^":
                setForegroundColor(200, 200, 200)
            if maparr[i][j] == "f":
                setForegroundColor(0, 255, 64)
            putChar(maparr[i][j], i, j)

def doCALandshit():
    maparr = [["~"] * (MAP_HEIGHT + 1) for _ in range(MAP_WIDTH + 1)]
    #land
    addLandscapeElements(maparr, TOTAL_LAND_AUTOMS, ".", ["~"], LAND_CYCLES, True)
    #mountains
    addLandscapeElements(maparr, TOTAL_MNT_AUTOMS, "^", ["."], MNT_CYCLES)
    # forest
    addLandscapeElements(maparr, TOTAL_FOREST_AUTOMS, "f", [".", "^"], FOREST_CYCLES)
    setForegroundColor(255, 255, 255)
    drawMap(maparr)
    #drawCharArray(maparr)
