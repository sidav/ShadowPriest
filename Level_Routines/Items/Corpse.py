from .Item import Item
from Message_Log import MessageLog as LOG


class Corpse(Item):
    _appearance = '&'
    _stackable = False
    _weight = 25
    _inventory = None

    def __init__(self, x, y, color, name='Unidentified Corpse', inventory = None):
        self._pos_x = x
        self._pos_y = y
        self._color = color
        self._name = name
        if inventory is None:
            LOG.append_error_message('Corpse created without an inventory!')
        else:
            self._inventory = inventory

    def is_body(self):
        return True
