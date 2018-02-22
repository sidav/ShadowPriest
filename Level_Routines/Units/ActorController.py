from Level_Routines import LevelController as LC
from ..Units import ActorController_Detection as AC_D, TurnCosts as TC
from Routines import SidavRandom as RND


# Controls AI-controlled units.


def control(lvl, current_actor):
    decide_state(lvl, current_actor)
    if current_actor.current_state == current_actor.states.calm:
        do_roam(lvl, current_actor)
    else:
        current_actor.spend_turns_for_action(TC.cost_for('wait'))


def decide_state(lvl, actor):
    state_turns_left = actor.get_current_state_expiration_turn() - lvl.get_current_turn()
    player = lvl.get_player()
    px, py = player.get_position()
    if AC_D.is_unit_seeing_position(lvl, actor, px, py):
        actor.set_current_state(actor.states.alerted, lvl.get_current_turn() + 250)
    elif state_turns_left > 0 and actor.get_current_state() == actor.states.alerted:
        actor.set_current_state(actor.states.distracted)
    elif state_turns_left <= 0:
        actor.set_current_state(actor.states.calm)
    else:
        pass
        # actor.set_current_state(actor.states.calm)


def do_roam(lvl, actor): # just roam around if the actor is in calm state
    posx, posy = actor.get_position()
    lookx, looky = actor.get_look_direction()
    # everything after "and" is an experimental behaviour. TODO: decide whether to remove or not that.

    if lvl.is_door_present(posx - lookx, posy - looky) and not lvl.is_door_closed(posx - lookx, posy - looky):
        LC.try_close_door(posx - lookx, posy - looky)
        actor.spend_turns_for_action(TC.cost_for('close door'))

    elif lvl.is_tile_passable(posx + lookx, posy+looky) and (lvl.is_tile_passable(posx + 2 * lookx, posy + 2 * looky) or lvl.is_door_present(posx + 2 * lookx, posy+2*looky)):
        actor.move_forward()
        actor.spend_turns_for_action(TC.cost_for('move'))
        if actor.was_rotated_previous_turn:
            actor.was_rotated_previous_turn = False
            actor.prefers_clockwise_rotation = RND.rand_bool()

    elif lvl.is_door_present(posx + lookx, posy+looky) and lvl.is_door_closed(posx + lookx, posy+looky):
        LC.try_open_door(posx + lookx, posy+looky)
        actor.spend_turns_for_action(TC.cost_for('open door'))
    else:
        actor.rotate_45_degrees(actor.prefers_clockwise_rotation)
        actor.spend_turns_for_action(TC.cost_for('turn'))
        actor.was_rotated_previous_turn = True
