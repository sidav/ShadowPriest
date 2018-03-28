from . import LevelController as LC
from .Event import Event
from .Units.Unit import Unit
from .Player import Player


def melee_attack_event(attacker, victim, other_text):
    att_name = attacker.get_name()
    vic_name = victim.get_name()
    if attacker.__class__.__name__ == 'Player':
        att_name = 'I'
        other_text = 'hit the'
    text = '{} {} {}!'.format(att_name, other_text, vic_name)
    event = Event(text, True, 0, LC.get_current_turn()+1)
    return event

def action(acting_unit, text):
    text = '{} {}.'.format(acting_unit.get_name(), text)
    event = Event(text, True, 0, LC.get_current_turn() + 1)
    return event