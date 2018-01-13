

# Represents (as superclass) the player, some character or enemy or what the heck you want to.
class Unit:

    _pos_x = _pos_y = 0
    _look_x = _look_y = 1
    _appearance = 'G'

    def __init__(self, posx, posy, appearance):
        self._pos_x = posx
        self._pos_y = posy
        pass

    def move_forward(self):
        # TODO
        pass

    def get_look_direction(self):
        return self._look_x, self._look_y

    def get_appearance(self):
        return self._appearance
