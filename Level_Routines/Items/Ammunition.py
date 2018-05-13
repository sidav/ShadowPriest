from .Item import Item


class Ammunition(Item):
    _stackable = True
    _base_damage_modifier = 0
    _damage_type = 0  # fuck knows what that mean.
    _ammunition_type = '9x19'  # fuck knows what that mean.

    def __init__(self, *args):
        super(Ammunition, self).__init__(*args)
        self._name = '9x19 ammo'

    def get_singular_name(self):
        return self._name

    def get_name(self):
        if self._quantity != 1:
            return '{}x {}'.format(self._quantity, self._name)
        else:
            return self._name

    def get_damage_modifier(self):
        return self._base_damage_modifier

    def is_of_type(self, type):
        if type == 'Ammo':
            return True
        else:
            return self.__class__.__name__ == type
