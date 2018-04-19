from .Item import Item


class Corpse(Item):
    _appearance = '&'
    _stackable = False
    _weight = 25

    def __init__(self, x, y, color, name='Unidentified Corpse'):
        self._pos_x = x
        self._pos_y = y
        self._color = color
        self._name = name

    def is_body(self):
        return True
