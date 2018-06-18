from .Item import Item
from ..Mechanics.StatusEffect import StatusEffect

class Potion(Item):

    def __init__(self, posx, posy, name='Unknown Potion', appearance='*', color=(192, 192, 0)):
        self._name = name
        self._pos_x, self._pos_y = posx, posy
        self._appearance = '!'
        if self._name == 'Potion of healing':
            self._status_effect_name = 'HEALING'
            self._status_effect_duration = 300
        elif self._name == 'Potion of poison':
            self._status_effect_name = 'POISON'
            self._status_effect_duration = 300

    def get_status_effect_name(self):
        return self._status_effect_name

    def get_status_effect_duration(self):
        return self._status_effect_duration

    def is_of_type(self, type):
        if type == 'Potion':
            return True
        return False
