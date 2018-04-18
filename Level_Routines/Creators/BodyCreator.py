from ..Units import Unit
from ..Items.Corpse import Corpse
from ..Items.UnconsciousBody import UnconsciousBody


def create_corpse_from_unit(unit):
    coords = unit.get_position()
    color = unit.get_color()
    name = unit.get_name() + ' corpse'
    corpse = Corpse(coords[0], coords[1], color, name)
    return corpse


def create_unconscious_body_from_unit(unit, KO_time):
    coords = unit.get_position()
    color = unit.get_color()
    name = 'Unconscious ' + unit.get_name()
    print(KO_time)
    body = UnconsciousBody(coords[0], coords[1], color, unit, name, time_for_wake_up=KO_time)
    return body