from ..Items.Potion import Potion
from Routines import SidavRandom as RAND


def random_beneficial_potion():
    select = RAND.rand(100)
    if select < 50:
        return Potion(0, 0, 'HEALING')
    else:
        return Potion(0, 0, 'PAINKILLER')
