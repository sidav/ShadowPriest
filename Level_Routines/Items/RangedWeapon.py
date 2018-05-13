from .Item import Item


class RangedWeapon(Item):
    _stackable = False
    _base_damage = 1
    _base_time = 1
    _base_tohit = 50  # in percent
    _min_str_to_use = 3
    _two_handed = False
    _damage_type = 0  # fuck knows what that mean.
    _bullets_per_shot = 1
    # _uses_clips = False
    _ammunition_type = '9x19 ammo' # fuck knows what that mean.
    _max_ammunition = 6
    _current_ammunition = 6

    def __init__(self, *args):
        super(RangedWeapon, self).__init__(*args)
        self._stackable = False
        self._current_ammunition = self._max_ammunition
        self._appearance = chr(169)

    def get_current_ammunition(self):
        return self._current_ammunition

    def set_current_ammunition(self, ammo):
        self._current_ammunition = ammo

    def get_max_ammunition(self):
        return self._max_ammunition

    def get_base_damage(self):
        return self._base_damage

    def is_of_type(self, type):
        if type == 'Weapon':
            return True
        else:
            return self.__class__.__name__ == type
