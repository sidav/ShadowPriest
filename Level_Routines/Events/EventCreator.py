from Level_Routines.Controllers import LevelController as LC
from .Event import Event
from Level_Routines.Units.Unit import Unit
from Routines import SidavRandom as RND


def knockout_attack_event(attacker:Unit, victim:Unit):
    att_name = attacker.get_name()
    vic_name = victim.get_name()
    vic_x, vic_y = victim.get_position()  # Not a mistake: the attack event has the victim coords.

    if attacker.__class__.__name__ == 'Player':
        att_name = 'I'
        vis_attack_text = 'strangle the'
        heard_attack_text = 'hear a strangle'

    seen_text = '{} {} {}!'.format(att_name, vis_attack_text, vic_name)
    heard_text = '{} {}!'.format(att_name, heard_attack_text)
    expir_turn = LC.get_current_turn() + 1
    event = Event(vic_x, vic_y, seen_text, heard_text, expiration_turn=expir_turn)
    return event


def attack_with_bare_hands_event(attacker:Unit, victim:Unit):
    att_name = attacker.get_name()
    vic_name = victim.get_name()
    vic_x, vic_y = victim.get_position()  # Not a mistake: the attack event has the victim coords.

    if attacker.__class__.__name__ == 'Player':
        att_name = 'I'
        vis_attack_text = 'punch the'
        heard_attack_text = 'hear a hit'

    seen_text = '{} {} {}!'.format(att_name, vis_attack_text, vic_name)
    heard_text = '{} {}!'.format(att_name, heard_attack_text)
    expir_turn = LC.get_current_turn() + 1
    event = Event(vic_x, vic_y, seen_text, heard_text, expiration_turn=expir_turn)
    return event


def attack_with_melee_weapon_event(attacker:Unit, victim:Unit):
    att_name = attacker.get_name()
    vic_name = victim.get_name()
    vic_x, vic_y = victim.get_position() # Not a mistake: the attack event has the victim coords.
    weapon_name = attacker.get_inventory().get_equipped_weapon().get_name()

    if attacker.__class__.__name__ == 'Player':
        att_name = 'I'
        vis_attack_text = 'hit the'
        heard_attack_text = 'hear a hit'
        weapon_name = 'my '+weapon_name
        seen_text = '{} {} {} with {}!'.format(att_name, vis_attack_text, vic_name, weapon_name)
        heard_text = 'I {}!'.format(heard_attack_text)
    else:
        if victim.is_player():
            vis_attack_text = 'hits me'
            heard_attack_text = 'feel a blade in my guts!'
        else:
            vis_attack_text = 'hits {}'.format(vic_name)
            heard_attack_text = 'hear a hit!'
        weapon_name = 'his ' + weapon_name
        seen_text = '{} {} with {}!'.format(att_name, vis_attack_text, weapon_name)
        heard_text = 'I {}!'.format(heard_attack_text)

    expir_turn = LC.get_current_turn()+1
    event = Event(vic_x, vic_y, seen_text, heard_text, expiration_turn=expir_turn)
    return event


def ranged_attack_event(attacker:Unit, victim:Unit):
    att_name = attacker.get_name()
    vic_name = victim.get_name()
    vic_x, vic_y = victim.get_position() # Not a mistake: the attack event has the victim coords.
    weapon_name = attacker.get_inventory().get_equipped_weapon().get_name()

    if attacker.__class__.__name__ == 'Player':
        att_name = 'I'
        vis_attack_text = 'shoot at the'
        heard_attack_text = 'hear a hit'
        weapon_name = 'my '+weapon_name
    else:
        weapon_name = 'a '+attacker.get_inventory().get_equipped_weapon().get_name(False)
        if victim.is_player():
            vic_name = 'me'
            vis_attack_text = 'shoots at'
            heard_attack_text = '\'m being shot!'
        else:
            vis_attack_text = 'shoots at {}'.format(vic_name)
            heard_attack_text = 'hear a bang!'

    seen_text = '{} {} {} with {}!'.format(att_name, vis_attack_text, vic_name, weapon_name)
    heard_text = '{} {}!'.format(att_name, heard_attack_text)
    expir_turn = LC.get_current_turn()+1
    event = Event(vic_x, vic_y, seen_text, heard_text, expiration_turn=expir_turn)
    return event


def missed_ranged_attack_event(attacker:Unit, victim:Unit):
    att_name = attacker.get_name()
    vic_name = victim.get_name()
    vic_x, vic_y = victim.get_position() # Not a mistake: the attack event has the victim coords.
    weapon_name = attacker.get_inventory().get_equipped_weapon().get_name()

    if attacker.__class__.__name__ == 'Player':
        att_name = 'I'
        vis_attack_text = 'miss the'
        heard_attack_text = 'shoot'
        weapon_name = 'my '+weapon_name

    seen_text = '{} {} {} with {}!'.format(att_name, vis_attack_text, vic_name, weapon_name)
    heard_text = '{} {}!'.format(att_name, heard_attack_text)
    expir_turn = LC.get_current_turn()+1
    event = Event(vic_x, vic_y, seen_text, heard_text, expiration_turn=expir_turn)
    return event


def empty_ammo_shooting_event(attacker, sound):
    att_x, att_y = attacker.get_position()
    seen_text = sound
    heard_text = sound
    expir_turn = LC.get_current_turn()+1
    event = Event(att_x, att_y, seen_text, heard_text, expiration_turn=expir_turn)
    return event


def stab_event(attacker:Unit, victim:Unit):
    att_name = attacker.get_name()
    vic_name = victim.get_name()
    vic_x, vic_y = victim.get_position()  # Not a mistake: the stab event has the victim coords.
    weapon_name = attacker.get_inventory().get_equipped_weapon().get_name()
    heard_attack_text = 'hear a blade swinging'

    if attacker.__class__.__name__ == 'Player':
        heard_attack_text = 'hear a blade swinging'
        msg = RND.rand(3)
        if msg == 0:
            seen_text = "I cut the {}'s throat with my {}!".format(vic_name, weapon_name)
        if msg == 1:
            seen_text = "I skewer the {} like a kebab!".format(vic_name)
        if msg == 2:
            seen_text = "{} convulces in agony! I put my {} out of his body.".format(vic_name, weapon_name)

    # seen_text = "{} {} {}'s throat with {}!".format(att_name, vis_attack_text, vic_name, weapon_name)
    heard_text = '{} {}!'.format(att_name, heard_attack_text)
    expir_turn = LC.get_current_turn() + 1
    event = Event(vic_x, vic_y, seen_text, heard_text, expiration_turn=expir_turn, hear_radius=2)
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

    expir_turn = LC.get_current_turn() + 1
    seen_text = '{} {}{} {}.'.format(name, action, ending, text)
    heard_text = 'I hear a sound of {} {}ing'.format(text, action)

    event = Event(x, y, seen_text, heard_text, hear_radius=hear_radius, expiration_turn=expir_turn)
    return event


def shout_event(shouting_unit, x, y, text, loudness):
    event = Event(x, y, text, text, False, loudness)
    return event
