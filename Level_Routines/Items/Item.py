

class Item:
    _appearance = '*'
    _color = (192, 192, 0)
    _name = 'Unknown Item'
    _pos_x, _pos_y = 0, 0
    _weight = 1

    def __init__(self, posx, posy, appearance='*', color=(192, 192, 0), name='Unknown Item', weight=1):
        self._pos_x = posx
        self._pos_y = posy
        self._appearance = appearance
        self._color = color
        self._name = name
        self._weight = weight

    def set_position(self, x, y):
        self._pos_x, self._pos_y = x, y

    def get_position(self):
        return self._pos_x, self._pos_y

    def get_name(self):
        return self._name

    def get_color(self):
        return self._color

    def get_appearance(self):
        return self._appearance
