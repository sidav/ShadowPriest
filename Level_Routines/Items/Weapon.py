from .Item import Item


class Weapon(Item):
    _stackable = False
    _base_damage = 1
    _base_stab_damage = 25
    _base_time = 1
    _base_tohit = 50  # in percent
    _min_str_to_use = 3
    _two_handed = False
    _damage_type = 0  # fuck knows what that mean.

    def __init__(self, *args):
        super(Weapon, self).__init__(*args)
        self._stackable = False

    def get_base_damage(self):
        return self._base_damage
