from Level_Routines.Controllers import LevelController as LC, ActorController_Detection as AC_D
from Level_Routines.Mechanics import TurnCosts as TC
from ..Events import EventCreator as EC
from Routines import SidavRandom as RND, AStarPathfinding as ASP
from . import UnitController as UC
from Message_Log import MessageLog as LOG
from Routines import SidavLOS as LOS


# Controls AI-controlled units at low level of abstraction.

def do_roam(lvl, actor): # just roam around if the actor is in calm state
    posx, posy = actor.get_position()
    lookx, looky = actor.get_look_direction()

    # reload weapon if needed.
    if try_reload(actor):
        return

    # close opened door behind.
    if lvl.is_door_present(posx - lookx, posy - looky) and not lvl.is_door_closed(posx - lookx, posy - looky):
        LC.try_close_door(actor, posx - lookx, posy - looky)

    #
    elif lvl.is_tile_passable(posx + lookx, posy+looky) and (
            lvl.is_tile_passable(posx + 2 * lookx, posy + 2 * looky) or lvl.is_door_present(posx + 2 * lookx, posy+2*looky)
    ):
        UC.try_move_forward(actor)
        if actor.was_rotated_previous_turn:
            actor.was_rotated_previous_turn = False
            actor.prefers_clockwise_rotation = RND.rand_bool()

    elif lvl.is_door_present(posx + lookx, posy+looky) and lvl.is_door_closed(posx + lookx, posy+looky) and \
            UC.can_unit_open_door(actor, posx + lookx, posy+looky):
        LC.try_open_door(actor, posx + lookx, posy+looky)
    else:
        actor.rotate_45_degrees(actor.prefers_clockwise_rotation)
        actor.spend_turns_for_action(TC.cost_for('turn'))
        actor.was_rotated_previous_turn = True


def do_engage(lvl, actor): # try to engage (and maybe attack) an enemy. The enemy is in "target_unit" field.
    ax, ay = actor.get_position()
    enemy = actor.get_target_unit()
    ex, ey = enemy.get_position()

    if can_effectively_shoot_at(actor, enemy):
        LC.ranged_attack(actor, ex, ey)
        return

    nextx, nexty = ASP.get_next_step_to_target(LC.get_passability_map_for(actor), ax, ay, ex, ey)
    UC.try_make_directional_action(lvl, actor, nextx, nexty)


# def do_pursue(lvl, actor): # pursue an enemy which have disappeared from actor's FOV.
#     ax, ay = actor.get_position()
#     enemy = actor.get_target_unit()
#     ex, ey = enemy.get_position()
#     nextx, nexty = ASP.get_next_step_to_target(LC.get_passability_map_for(actor), ax, ay, ex, ey)
#     UC.try_make_directional_action(lvl, actor, nextx, nexty)


def do_search(lvl, actor): # search for an enemy which have disappeared from actor's FOV.
    ax, ay = actor.get_position()
    tx, ty = actor.get_target_coords()
    if (ax, ay) == (tx, ty):
        lookx = RND.rand(3) - 1
        looky = RND.rand(3) - 1
        UC.rotate_to_coords(actor, lookx, looky)
        return
    nextx, nexty = ASP.get_next_step_to_target(LC.get_passability_map_for(actor), ax, ay, tx, ty)
    UC.try_make_directional_action(lvl, actor, nextx, nexty)

# TODO: make do_investigate


def do_shout_for_attention_to(shouting_unit, x, y, text, loudness, time=0):
    event = EC.shout_event(shouting_unit, x, y, text, loudness)
    LC.add_event_to_stack(event)
    shouting_unit.spend_turns_for_action(time)


def try_reload(attacker):
    attacker_weapon = attacker.get_inventory().get_equipped_weapon()
    if attacker_weapon is None or not attacker_weapon.is_of_type('RangedWeapon'):
        return False
    ammo = attacker_weapon.get_loaded_ammunition()
    if ammo is None or ammo.get_quantity() == 0:
        return LC.try_reload_unit_weapon(attacker)
    return False


def can_effectively_shoot_at(attacker, victim):
    a_x, a_y = attacker.get_position()
    v_x, v_y = victim.get_position()
    attacker_weapon = attacker.get_inventory().get_equipped_weapon()

    if attacker_weapon is None or not attacker_weapon.is_of_type('RangedWeapon'):
        return False

    ammo = attacker_weapon.get_loaded_ammunition()

    if ammo is not None and ammo.get_quantity() == 0:
        return False
    if not LOS._straightLOSCheck(a_x, a_y, v_x, v_y): # We use simpler method first to save calculation time...
        print('AI: Using heavy LOS calculations!')
        vis_table = LOS.getVisibilityTableFromPosition(a_x, a_y) # ...and if that does not help, use heavy calculations.
        if not vis_table[v_x][v_y]:
            return False
    return True