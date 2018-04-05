from Level_Routines import LevelController as LC
from .Event import Event
from Level_Routines.Units.Unit import Unit
from Level_Routines.Player import Player


def melee_attack_event(attacker, victim):
    att_name = attacker.get_name()
    vic_name = victim.get_name()
    vic_x, vic_y = victim.get_position() # Not a mistake: the attack event has the victim coords.

    if attacker.__class__.__name__ == 'Player':
        att_name = 'I'
        vis_attack_text = 'hit the'
        heard_attack_text = 'hear a hit'

    seen_text = '{} {} {}!'.format(att_name, vis_attack_text, vic_name)
    heard_text = '{} {}!'.format(att_name, heard_attack_text)
    expir_turn = LC.get_current_turn()+10
    event = Event(vic_x, vic_y, seen_text, heard_text, expiration_turn=expir_turn)
    return event


def action_event(acting_unit, action, text='', hear_radius = 0):
    # TODO: coordinates for (for example) 'close door' or 'open door' events aren't quite adequate, because
    # TODO: player sees the event when he sees acting_unit, but not when he sees the door only!
    # TODO: he still properly hears the event, though.
    x, y = acting_unit.get_position()
    if acting_unit.__class__.__name__ == 'Player':
        name = 'I'
        ending = ''
    else:
        name = acting_unit.get_name()
        ending = 's'

    expir_turn = LC.get_current_turn() + 10
    seen_text = '{} {}{} {}.'.format(name, action, ending, text)
    heard_text = 'I hear a sound of {} {}ing.'.format(text, action)

    event = Event(x, y, seen_text, heard_text, hear_radius=hear_radius, expiration_turn=expir_turn)
    return event