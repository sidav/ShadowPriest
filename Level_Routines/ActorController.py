from Routines import SidavRandom as RND
from . import LevelController as LC, ActorController_Detection as AC_D
from Message_Log import MessageLog as LOG
# Controls AI-controlled units.


def decide_state(lvl, actor):
    player = lvl.get_player()
    px, py = player.get_position()
    if AC_D.is_unit_seeing_position(lvl, actor, px, py):
        actor.set_current_state(actor.states.alerted, 25)
    elif actor.get_current_state_timeout() > 0:
        actor.set_current_state(actor.states.distracted)
    else:
        actor.set_current_state(actor.states.calm)


def pick_action_and_do(lvl):
    all_units = lvl.get_all_units()
    for current_actor in all_units:
        decide_state(lvl, current_actor)
        if current_actor.current_state == current_actor.states.calm:
            do_roam(lvl, current_actor)
        current_actor.decrease_current_state_timeout()


def do_roam(lvl, actor): # just roam around if the actor is in calm state
    posx, posy = actor.get_position()
    lookx, looky = actor.get_look_direction()
    # everything after "and" is an experimental behaviour. TODO: decide whether to remove or not that.

    if lvl.is_door_present(posx - lookx, posy - looky) and not lvl.is_door_closed(posx - lookx, posy - looky):
        LC.try_close_door(posx - lookx, posy - looky)

    elif lvl.is_tile_passable(posx + lookx, posy+looky) and (lvl.is_tile_passable(posx + 2 * lookx, posy + 2 * looky) or lvl.is_door_present(posx + 2 * lookx, posy+2*looky)):
        actor.move_forward()
        if actor.was_rotated_previous_turn:
            actor.was_rotated_previous_turn = False
            actor.prefers_clockwise_rotation = RND.rand_bool()

    elif lvl.is_door_present(posx + lookx, posy+looky) and lvl.is_door_closed(posx + lookx, posy+looky):
        LC.try_open_door(posx + lookx, posy+looky)

    else:
        actor.rotate_45_degrees(actor.prefers_clockwise_rotation)
        actor.was_rotated_previous_turn = True
