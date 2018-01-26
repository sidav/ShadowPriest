import Routines.SidavRandom as random

# Represents (as superclass) the player, some character or enemy or what the heck you want to.
class Unit:

    _pos_x = _pos_y = 0
    _look_x = _look_y = 0
    _has_look_direction = True # <-- is the "looking thingy" neccessary to draw?
    _appearance = 'G'

    def __init__(self, posx, posy, appearance = 'G'):
        self._appearance = appearance
        self._pos_x = posx
        self._pos_y = posy
        while self._look_x == 0 and self._look_y == 0:
            self._look_x = random.rand(3) - 1
            self._look_y = random.rand(3) - 1
        pass

    def move_forward(self):
        self._pos_x += self._look_x
        self._pos_y += self._look_y
        pass

    def move_by_vector(self, x, y):
        self._pos_x += x
        self._pos_y += y
        pass

    def rotate_90_degrees(self, clockwise=True):
        temp_x = self._look_x
        if clockwise:
            self._look_x = - self._look_y
            self._look_y = temp_x
        else:
            self._look_x = self._look_y
            self._look_y = - temp_x

    def rotate_45_degrees(self, clockwise=True):
        temp_x = self._look_x
        if clockwise:
            self._look_x += - self._look_y
            self._look_y += temp_x
        else:
            self._look_x = self._look_y
            self._look_y = - temp_x

        if self._look_x != 0:
            self._look_x //= abs(self._look_x)
        if self._look_y != 0:
            self._look_y //= abs(self._look_y)

    def has_look_direction(self):
        return self._has_look_direction

    def get_position(self):
        return self._pos_x, self._pos_y

    def get_look_direction(self):
        return self._look_x, self._look_y

    def get_appearance(self):
        return self._appearance
