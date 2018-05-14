from .Item import Item


class Ammunition(Item):
    _stackable = True
    _base_ranged_damage_modifier = 0
    _damage_type = 0  # fuck knows what that mean.
    _ammunition_type = '9x19'  # fuck knows what that mean.

    def __init__(self, posx, posy, name='UNIDENTIFIED AMMO', type='UNSET TYPE', color=(192, 160, 32),
                 quantity=1, appearance='/', weight=1):
        stackable = True
        self._ammunition_type = type
        super(Ammunition, self).__init__(posx, posy, appearance, color, name, weight, stackable, quantity)

    def get_singular_name(self):
        return self._name

    def get_name(self):
        if self._quantity != 1:
            return '{}x {}'.format(self._quantity, self._name)
        else:
            return self._name

    def is_stackable_with(self, item):
        if self._stackable:
            if item.is_of_type('Ammunition'):
                if item.get_singular_name() == self._name:
                    if self != item:
                        return True
        return False

    def get_ranged_damage_modifier(self):
        return self._base_ranged_damage_modifier

    def get_ammunition_type(self):
        return self._ammunition_type

    def is_of_type(self, type):
        if type == 'Ammo':
            return True
        else:
            return self.__class__.__name__ == type
