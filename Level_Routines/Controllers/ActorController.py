from Level_Routines.Controllers import LevelController as LC, ActorController_Detection as AC_D
from Level_Routines.Mechanics import TurnCosts as TC
from Routines import SidavRandom as RND, AStarPathfinding as ASP
from . import UnitController as UC


# Controls AI-controlled units at low level of abstraction.

def do_roam(lvl, actor): # just roam around if the actor is in calm state
    posx, posy = actor.get_position()
    lookx, looky = actor.get_look_direction()

    # Pathfinding debug code (delete it)
    tx, ty = lvl.get_player().get_position()
    # print("target coords {},{}".format(tx, ty))
    nextx, nexty = ASP.get_next_step_to_target(LC.get_passability_map_for(actor), posx, posy, tx, ty)
    # print("moving towards {},{}".format(nextx, nexty))
    UC.try_make_directional_action(lvl, actor, nextx, nexty)
    return
    # /end of pthf debug


    # everything after "and" is an experimental behaviour. TODO: decide whether to remove or not that.

    if lvl.is_door_present(posx - lookx, posy - looky) and not lvl.is_door_closed(posx - lookx, posy - looky):
        LC.try_close_door(actor, posx - lookx, posy - looky)
        actor.spend_turns_for_action(TC.cost_for('close door'))

    elif lvl.is_tile_passable(posx + lookx, posy+looky) and (lvl.is_tile_passable(posx + 2 * lookx, posy + 2 * looky) or lvl.is_door_present(posx + 2 * lookx, posy+2*looky)):
        UC.try_move_forward(actor)
        if actor.was_rotated_previous_turn:
            actor.was_rotated_previous_turn = False
            actor.prefers_clockwise_rotation = RND.rand_bool()

    elif lvl.is_door_present(posx + lookx, posy+looky) and lvl.is_door_closed(posx + lookx, posy+looky):
        LC.try_open_door(actor, posx + lookx, posy+looky)
        actor.spend_turns_for_action(TC.cost_for('open door'))
    else:
        actor.rotate_45_degrees(actor.prefers_clockwise_rotation)
        actor.spend_turns_for_action(TC.cost_for('turn'))
        actor.was_rotated_previous_turn = True
