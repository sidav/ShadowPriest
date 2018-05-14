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
    allowed_ammunition_type = '9x19'  # fuck knows what that mean.
    _loaded_ammunition = None
    _max_ammunition = 6

    def __init__(self, *args):
        super(RangedWeapon, self).__init__(*args)
        self._base_stab_damage = 0
        self._stackable = False
        self._current_ammunition = 0
        self._appearance = chr(169)

    def get_remaining_ammunition_count(self):
        if self._loaded_ammunition is not None:
            return self._loaded_ammunition.get_quantity()
        else:
            return 0

    def get_name(self, show_remaining_ammo=True):
        if show_remaining_ammo:
            return "{}({}/{})".format(self._name, self.get_remaining_ammunition_count(), self._max_ammunition)
        else:
            return self._name

    def get_base_ranged_damage(self):
        return self._base_ranged_damage

    def get_loaded_ammunition(self):
        return self._loaded_ammunition

    def load_ammunition(self, ammo):
        self._loaded_ammunition = ammo

    def can_be_refilled_with(self, ammo):
        return self._loaded_ammunition is not None and \
               self.can_be_loaded_with(ammo) and self._loaded_ammunition.is_stackable_with(ammo)

    def can_be_loaded_with(self, ammo):
        return self.allowed_ammunition_type == ammo.get_ammunition_type()

    def get_max_ammunition(self):
        return self._max_ammunition

    def get_base_melee_damage(self):
        return self._base_melee_damage

    def is_of_type(self, type):
        if type == 'Weapon':
            return True
        else:
            return self.__class__.__name__ == type
