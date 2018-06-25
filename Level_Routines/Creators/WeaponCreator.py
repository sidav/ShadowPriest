from ..Items.MeleeWeapon import MeleeWeapon
from ..Items.RangedWeapon import RangedWeapon


def create_club(x, y, usual=True):
    weapon = MeleeWeapon(x, y)
    weapon._appearance = ')'
    weapon._color = (128, 96, 0)
    weapon._name = 'club'
    weapon._base_melee_damage = 8
    weapon._base_stab_damage = 0
    weapon._base_time = 1
    weapon._base_tohit = 65  # in percent
    weapon._min_str_to_use = 2
    return weapon


def create_dagger(x, y, usual=True):
    weapon = MeleeWeapon(x, y)
    weapon._appearance = ')'
    weapon._color = (32, 64, 192)
    weapon._name = 'dagger'
    weapon._base_melee_damage = 16
    weapon._base_stab_damage = 100
    weapon._base_time = 1
    weapon._base_tohit = 65  # in percent
    weapon._min_str_to_use = 2
    return weapon


def create_revolver(x, y, usual=True):
    weapon = RangedWeapon(x, y)
    weapon._name = 'revolver'
    return weapon