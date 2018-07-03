from .Item import Item
from ..Mechanics.StatusEffect import StatusEffect


class Potion(Item):

    def __init__(self, posx, posy, effect='Unknown', appearance='*', color=(192, 192, 0)):
        self._pos_x, self._pos_y = posx, posy
        self._appearance = '!'
        self._name = effect.capitalize() + ' potion'
        self._status_effect_name = effect.upper()

        # TODO: separate data file for all potions' durations
        if self._status_effect_name == 'HEALING':
            self._status_effect_duration = 300
        elif self._status_effect_name == 'POISON':
            self._status_effect_duration = 900
        elif self._status_effect_name == 'PAINKILLER':
            self._status_effect_duration = 250
        else:
            self._status_effect_duration = 1

    def get_status_effect_name(self):
        return self._status_effect_name.upper()

    def get_status_effect_duration(self):
        return self._status_effect_duration

    def is_of_type(self, type):
        if type == 'Potion':
            return True
        return False
