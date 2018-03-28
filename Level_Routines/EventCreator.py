from . import LevelController as LC
from .Event import Event
from .Units.Unit import Unit


def attack(attacker, victim, other_text):
    text = '{} {} {}!'.format(attacker.get_name(), other_text, victim.get_name())
    event = Event(text, True, 0, LC.get_current_turn()+1)
    return event

def action(acting_unit, text):
    text = '{} {}.'.format(acting_unit.get_name(), text)
    event = Event(text, True, 0, LC.get_current_turn() + 1)
    return event