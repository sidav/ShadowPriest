import tdl
from sys import exit as closeProgram

_SCREEN_WIDTH = 80#80 is default
_SCREEN_HEIGHT = 25#25 is default

_LIMIT_FPS = 10  # 20 frames-per-second maximum

try:
    tdl.set_font('shadowpriest8x12_gs_ro.png', greyscale=True, altLayout=False)
except:
    print("Oh fuck, the font is missing!")
    closeProgram()
    pass

#console = tdl.init(_SCREEN_WIDTH, _SCREEN_HEIGHT, title="Roguelike", fullscreen= False, renderer= "SDL")
FORECOLOR = (255,255,255)
BACKCOLOR = (0, 0, 0)

# LAST_KEY_PRESSED = tdl.event

def initConsole(SW, SH, titleString):
    global _SCREEN_WIDTH, _SCREEN_HEIGHT
    _SCREEN_WIDTH = SW
    _SCREEN_HEIGHT = SH
    global console
    console = tdl.init(SW, SH, title=titleString, fullscreen=False, renderer="SDL")
    tdl.set_fps(_LIMIT_FPS)
    clearConsole()
    flushConsole()


def putChar(char, x, y):
    console.draw_char(x, y, char, bg=BACKCOLOR, fg=FORECOLOR)


def putString(string, x, y):
    console.draw_str(x, y, string, bg=BACKCOLOR, fg=FORECOLOR)


def put_wrapped_text_in_rect(text, x, y, w, h):
    words = text.split()
    curr_line = 0
    curr_line_length = 0
    for word in words:
        if curr_line_length + len(word) >= w:
            curr_line += 1
            curr_line_length = 0
            if curr_line == h:
                return
        putString(word+' ', x+curr_line_length, y + curr_line)
        curr_line_length += len(word) + 1


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
            if x < _SCREEN_WIDTH and y < _SCREEN_HEIGHT:
                putChar(arr[x][y], x, y)


def drawCharArrayAtPosition(arr, xpos, ypos, transpose=False):
    if transpose:
        for y in range(len(arr)):
            putString(arr[y],xpos,y+ypos)
            # for y in range(len(arr[x])):
            #     if x < _SCREEN_WIDTH and y < _SCREEN_HEIGHT:
            #         putChar(arr[x][y], y + ypos, x + xpos)
    else:
        for x in range(len(arr)):
            for y in range(len(arr[x])):
                if x < _SCREEN_WIDTH and y < _SCREEN_HEIGHT:
                    putChar(arr[x][y], x+xpos, y+ypos)


def setBackgroundColor(r, g=-1, b=-1):
    global BACKCOLOR
    if g != -1 and b != -1:
        BACKCOLOR = (r, g, b)
    else:
        BACKCOLOR = (r[0], r[1], r[2])


def setForegroundColor(r, g = -1, b = -1):
    global FORECOLOR
    if g != -1 and b != -1:
        FORECOLOR = (r, g, b)
    else:
        FORECOLOR = (r[0], r[1], r[2])



def flushConsole():
    tdl.flush()


def clearConsole():
    console.clear(bg = (0, 0, 0), fg = (0, 0, 0))


def isWindowClosed():
    return tdl.event.is_window_closed()


def readKey():
    global LAST_KEY_PRESSED
    while not tdl.event.is_window_closed():
        LAST_KEY_PRESSED = tdl.event.key_wait()
        print("text: '{}', char: '{}', keychar: '{}'".format(LAST_KEY_PRESSED.text, LAST_KEY_PRESSED.char, LAST_KEY_PRESSED.keychar))
        if LAST_KEY_PRESSED.keychar == 'TEXT' or LAST_KEY_PRESSED.keychar.__contains__('F') or \
            LAST_KEY_PRESSED.keychar == 'DOWN' or LAST_KEY_PRESSED.keychar == 'UP' or LAST_KEY_PRESSED.keychar.__contains__('ENTER') \
                or LAST_KEY_PRESSED.keychar == 'ESCAPE' or LAST_KEY_PRESSED.keychar == 'BACKSPACE':
            break
        else:
            print('KEY REJECTED.')
    if tdl.event.is_window_closed():
        closeProgram(0)
    return LAST_KEY_PRESSED

# def wait_for_key_press():
#         pass
