from ..Units import Unit
from ..Items.Corpse import Corpse


def create_corpse_from_unit(unit):
    coords = unit.get_position()
    color = unit.get_color()
    name = unit.get_name() + ' corpse'
    corpse = Corpse(coords[0], coords[1], color, name)
    return corpse
