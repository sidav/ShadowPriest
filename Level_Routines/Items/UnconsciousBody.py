from Message_Log import MessageLog as LOG
from .Item import Item


class UnconsciousBody(Item):
    _appearance = '%'
    _stackable = False
    _weight = 25
    _time_for_wake_up = 0
    _unit = None  # needed for waking up
    _searched = False

    def __init__(self, x, y, color, unit, name='Unidentified KOed Body', time_for_wake_up = -1):
        self._pos_x = x
        self._pos_y = y
        self._color = color
        self._name = name
        self._time_for_wake_up = time_for_wake_up
        if time_for_wake_up == -1:
            LOG.append_error_message('KOed body created with no KO time!')
        self._unit = unit

    def get_time_for_wake_up(self):
        return self._time_for_wake_up

    def get_original_unit(self):
        return self._unit

    def get_inventory(self):
        return self._unit.get_inventory()

    def empty_backpack(self):
        self._unit.get_inventory().backpack = []

    def is_body(self):
        return True

    def set_searched(self, set=True):
        self._searched = set

    def get_searched(self):
        return self._searched

    def is_of_type(self, type):
        if type == 'Body' or type == 'UnconsciousBody':
            return True
        return False

    def get_name(self):
        name = self._name
        if self._searched:
            name += ' (searched)'
        return name
