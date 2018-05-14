from .Item import Item


class MeleeWeapon(Item):
    _stackable = False
    _base_melee_damage = 1
    _base_stab_damage = 25
    _base_time = 1
    _base_tohit = 50  # in percent
    _min_str_to_use = 3
    _two_handed = False
    _damage_type = 0  # fuck knows what that mean.

    def __init__(self, *args):
        super(MeleeWeapon, self).__init__(*args)
        self._stackable = False

    def get_base_melee_damage(self):
        return self._base_melee_damage

    def get_base_stab_damage(self):
        return self._base_stab_damage

    def is_stabbing(self):
        return self._base_stab_damage > 0

    def is_of_type(self, type):
        if type == 'Weapon':
            return True
        else:
            return self.__class__.__name__ == type
