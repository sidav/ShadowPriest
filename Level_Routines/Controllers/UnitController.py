from GLOBAL_DATA import Global_Constants as GC
from Level_Routines.Mechanics import TurnCosts as TC, StatusEffect as SE
from Level_Routines.Events import EventCreator as EC
from Level_Routines.Events.EventsStack import EventsStack as ESTCK
from Message_Log import MessageLog as LOG
from Routines import TdlConsoleWrapper as CW, SidavLOS as LOS
from Level_Routines import LevelView
from Level_Routines.Creators import BodyCreator
from Level_Routines.LevelInitializer import initialize_level
from Level_Routines.LevelModel import LevelModel
from Level_Routines.Mechanics import MeleeAttack, Knockout, RangedAttack
from Level_Routines.Player import Statusbar
from . import LevelController as LC, PlayerController as P_C, ActorController as A_C, StatusEffectsController as SE_C
from Level_Routines.Units.Unit import Unit

levelmodel = None


# All unit actions (when they're applicable for both player and actors) are here.


def get_sight_range(unit):
    adv = unit.get_rpg_stats().get_advertence()
    MIN_RANGE = 4
    PLAYER_BONUS = 3
    looking_range = MIN_RANGE + (adv + PLAYER_BONUS) // 2 if unit.is_of_type('Player') else MIN_RANGE + (adv // 2)
    return looking_range


def set_current_level(level):
    global levelmodel
    levelmodel = level


def can_unit_open_door(unit, x, y):
    door_lock = LC.get_tile_lock_level(x, y)
    return unit.get_inventory().has_key_of_lock_level(door_lock)


def make_noise(unit, text1, text2, loudness, time=0):
    event = EC.action_event(unit, text1, text2, loudness)
    LC.add_event_to_stack(event)
    unit.spend_turns_for_action(time)


def try_move_forward(unit):
    posx, posy = unit.get_position()
    lookx, looky = unit.get_look_direction()
    if levelmodel.is_tile_passable(posx + lookx, posy + looky):
        unit.move_forward()
        unit.spend_turns_for_action(TC.cost_for('move'))
        return True
    return False


def try_move_by_vector(unit, x, y):
    posx, posy = unit.get_position()
    if levelmodel.is_tile_passable(posx + x, posy + y):
        unit.move_by_vector(x, y)
        unit.spend_turns_for_action(TC.cost_for('move'))
        return True
    return False


def rotate_to_coords(unit, x, y):
    if not (x == y == 0):
        unit.set_look_direction(x, y)
        unit.spend_turns_for_action(TC.cost_for('turn', unit))


def try_make_directional_action(lvl, unit, vect_x, vect_y): #turn or move or open door or attack
    posx, posy = unit.get_position()
    lookx, looky = unit.get_look_direction()
    if unit.has_look_direction() and (lookx, looky) != (vect_x, vect_y):
        # unit.rotate_45_degrees(unit.prefers_clockwise_rotation)
        rotate_to_coords(unit, vect_x, vect_y)
        return True
    else:
        x, y = posx + vect_x, posy + vect_y
        if lvl.is_tile_passable(x, y):
            try_move_by_vector(unit, vect_x, vect_y)
            return True
        elif LC.is_unit_present_at(x, y):
            potential_victim = LC.get_unit_at(x, y)
            if unit.get_faction() != potential_victim.get_faction():
                melee_attack(unit, potential_victim)
            return True
        else:
            success = LC.try_open_door(unit, x, y)
            return success
    return False


def melee_attack(attacker:Unit, victim:Unit):
    attacker_weapon = attacker.get_inventory().get_equipped_weapon()
    if attacker_weapon is None:
        attacker.spend_turns_for_action(TC.cost_for('Barehanded attack'))
        if MeleeAttack.try_to_attack_with_bare_hands(attacker, victim):
            event = EC.attack_with_bare_hands_event(attacker, victim)
    else:
        if victim.can_be_stabbed() and attacker_weapon.is_stabbing():
            attacker.spend_turns_for_action(TC.cost_for('stab'))
            if MeleeAttack.try_to_stab(attacker, victim):
                event = EC.stab_event(attacker, victim)
        elif MeleeAttack.try_to_attack_with_weapon(attacker, victim):
            attacker.spend_turns_for_action(TC.cost_for('melee attack'))
            event = EC.attack_with_melee_weapon_event(attacker, victim)
    LC.add_event_to_stack(event)


def quaff_a_potion(unit, potion):
    inv = unit.get_inventory()
    if potion.get_quantity() > 1:               # <-- DO SOMETHING WITH THAT KOSTYLI!!1
        potion.change_quantity_by(-1)           # <-- DO SOMETHING WITH THAT KOSTYLI!!1
    else:                                       # <-- DO SOMETHING WITH THAT KOSTYLI!!1
        inv.remove_item_from_backpack(potion)   # <-- DO SOMETHING WITH THAT KOSTYLI!!1
    SE_C.add_potion_status_effect_to_a_unit(potion, unit)
    LC.add_event_to_stack(EC.action_event(unit, 'quaff', 'a {}'.format(potion.get_singular_name()), 2))
    unit.spend_turns_for_action(TC.cost_for('quaffing', unit))
