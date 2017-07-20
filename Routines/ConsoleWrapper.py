import tdl

SCREEN_WIDTH = 80#80 is default
SCREEN_HEIGHT = 25#25 is default

LIMIT_FPS = 20  # 20 frames-per-second maximum

try:
    tdl.set_font('terminal8x12_gs_ro.png', greyscale=True, altLayout=False)
except:
    print("Oh fuck, the font is missing!")
    pass

#console = tdl.init(SCREEN_WIDTH, SCREEN_HEIGHT, title="Roguelike", fullscreen= False, renderer= "SDL")
FORECOLOR = (255,255,255)
BACKCOLOR = (0, 0, 0)

# LAST_KEY_PRESSED = tdl.event

def initConsole(SW, SH, titleString):
    global console
    console = tdl.init(SW, SH, title=titleString, fullscreen=False, renderer="SDL")
    clearConsole()
    flushConsole()


def putChar(char, x, y):
    console.draw_char(x, y, char, bg=BACKCOLOR, fg=FORECOLOR)


def putString(string, x, y):
    console.draw_str(x, y, string, bg=BACKCOLOR, fg=FORECOLOR)


def drawLine(x0, y0, x1, y1, chr = "#"):
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
            for x in range(fromx, tox + xmod, xmod):
                line.append(xy(x, y))
                error = error + deltaerr
                if 2 * error >= deltax:
                    y = y + ymod
                    error -= deltax
        elif deltay > deltax:
            x = fromx
            deltaerr = deltax
            for y in range(fromy, toy + ymod, ymod):
                line.append(xy(x, y))
                error = error + deltaerr
                if 2 * error >= deltay:
                    x = x + xmod
                    error -= deltay
        return line

    line = get_line(x0, y0, x1, y1)
    for i in line:
        putChar(chr, i.x, i.y)

def drawCircle(x0, y0, radius, chr = "#"):
    class xy:
        def __init__(self, x, y):
            self.x = x
            self.y = y

    def get_circle(x0, y0, radius):
        circle = []
        x = radius
        y = 0
        radiusError = 1 - x
        while (x >= y):
            circle.append(xy(x + x0, y + y0))
            circle.append(xy(y + x0, x + y0))
            circle.append(xy(-x + x0, y + y0))
            circle.append(xy(-y + x0, x + y0))
            circle.append(xy(-x + x0, -y + y0))
            circle.append(xy(-y + x0, -x + y0))
            circle.append(xy(x + x0, -y + y0))
            circle.append(xy(y + x0, -x + y0))
            y += 1
            if (radiusError < 0):
                radiusError += 2 * y + 1
            else:
                x -= 1
                radiusError += 2 * (y - x + 1)
        return circle

    circle = get_circle(x0, y0, radius)
    for i in circle:
        putChar(chr, i.x, i.y)

def drawRect(x0, y0, w, h):
    for i in range(x0, x0+w):
        putChar("#", i, y0)
        putChar("#", i, y0+h-1)
    for j in range(y0, y0+h):
        putChar("#", x0, j)
        putChar("#", x0+w-1, j)

def drawCharArray(arr):
    for x in range(len(arr)):
        for y in range(len(arr[x])):
            if x < SCREEN_WIDTH and y < SCREEN_HEIGHT:
                putChar(arr[x][y], x, y)


def drawCharArrayAtPosition(arr, xpos, ypos, transpose=False):
    if transpose:
        for y in range(len(arr)):
            putString(arr[y],xpos,y+ypos)
            # for y in range(len(arr[x])):
            #     if x < SCREEN_WIDTH and y < SCREEN_HEIGHT:
            #         putChar(arr[x][y], y + ypos, x + xpos)
    else:
        for x in range(len(arr)):
            for y in range(len(arr[x])):
                if x < SCREEN_WIDTH and y < SCREEN_HEIGHT:
                    putChar(arr[x][y], x+xpos, y+ypos)


def setBackgroundColor(r, g, b):
    global BACKCOLOR
    BACKCOLOR = (r, g, b)


def setForegroundColor(r, g, b):
    global FORECOLOR
    FORECOLOR = (r, g, b)



def flushConsole():
    tdl.flush()


def clearConsole():
    console.clear(bg = (0, 0, 0), fg = (0, 0, 0))


def isWindowClosed():
    return tdl.event.is_window_closed()


def readKey():
    global LAST_KEY_PRESSED
    LAST_KEY_PRESSED = tdl.event.key_wait()
    return LAST_KEY_PRESSED


