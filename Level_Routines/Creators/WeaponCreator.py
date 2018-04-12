from ..Items.Weapon import Weapon


def create_dagger(x, y, usual=True):
    weapon = Weapon(x, y)
    weapon._appearance = ')'
    weapon._color = (32, 64, 192)
    weapon._name = 'dagger'
    weapon._base_damage = 6
    weapon._base_stab_damage = 100
    weapon._base_time = 1
    weapon._base_tohit = 65  # in percent
    weapon._min_str_to_use = 2
    return weapon
