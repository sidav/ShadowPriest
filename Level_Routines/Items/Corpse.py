from .Item import Item
from Message_Log import MessageLog as LOG


class Corpse(Item):
    _appearance = '&'
    _stackable = False
    _weight = 25

    def __init__(self, x, y, color, name='Unidentified Corpse', inventory = None):
        self._pos_x = x
        self._pos_y = y
        self._color = color
        self._name = name
        self._searched = False
        self._was_already_seen_by_AI = False
        if inventory is None:
            LOG.append_error_message('Corpse created without an inventory!')
        else:
            self._inventory = inventory

    def is_body(self):
        return True

    def get_inventory(self):
        return self._inventory

    def empty_backpack(self):
        self._inventory.backpack = []

    def get_was_seen_by_ai(self):
        return self._was_already_seen_by_AI

    def set_was_seen_by_ai(self, seen=True):
        self._was_already_seen_by_AI = seen

    def set_searched(self, set=True):
        self._searched = set

    def get_searched(self):
        return self._searched

    def is_of_type(self, type):
        if type == 'Body' or type == 'Corpse':
            return True
        return False

    def get_name(self):
        name = self._name
        if self._searched:
            name += ' (searched)'
        return name
