from ..Items.Weapon import Weapon


def create_dagger(x, y, usual=True):
    weapon = Weapon(x, y)
    weapon._base_damage = 5
    return weapon