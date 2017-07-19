#Bresenham's algorithm.
#Needs to be more optimised to be FAST AS THE FUCKING HELL
#Anyway, it works even in its current state.

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
        y+=1
        if (radiusError < 0):
            radiusError += 2 * y + 1
        else:
            x-=1
            radiusError += 2 * (y - x + 1)
    return circle