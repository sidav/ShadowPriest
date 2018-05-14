from .Item import Item
from .MeleeWeapon import MeleeWeapon


class RangedWeapon(MeleeWeapon):
    _stackable = False
    _base_melee_damage = 5
    _base_time = 10
    _base_tohit = 50  # in percent
    _min_str_to_use = 3
    _two_handed = False
    _damage_type = 0  # fuck knows what that mean.

    # only ranged weapon stuff below this comment

    _base_ranged_damage = 10
    _bullets_per_shot = 1
    # _uses_clips = False
    _ammunition_type = '9x19 ammo' # fuck knows what that mean.
    _max_ammunition = 6
    _current_ammunition = 0

    def __init__(self, *args):
        super(RangedWeapon, self).__init__(*args)
        self._base_stab_damage = 0
        self._stackable = False
        self._current_ammunition = 0
        self._appearance = chr(169)

    def get_name(self):
        return "{}({}/{})".format(self._name, self._current_ammunition, self._max_ammunition)

    def get_base_ranged_damage(self):
        return self._base_ranged_damage

    def get_current_ammunition(self):
        return self._current_ammunition

    def set_current_ammunition(self, ammo):
        self._current_ammunition = ammo

    def get_max_ammunition(self):
        return self._max_ammunition

    def get_base_melee_damage(self):
        return self._base_melee_damage

    def is_of_type(self, type):
        if type == 'Weapon':
            return True
        else:
            return self.__class__.__name__ == type
