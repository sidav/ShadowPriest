from Routines import SidavRandom as RND


# Controls AI-controlled units.

def pick_action_and_do(lvl):
    all_units = lvl.get_all_units()
    for current in all_units:
        if current.current_state == current.states.calm:
            do_roam(lvl, current)
        pass


def do_roam(lvl, actor): # just roam around if the actor is in calm state
    posx, posy = actor.get_position()
    lookx, looky = actor.get_look_direction()
    # everything after "and" is an experimental behaviour. TODO: decide whether to remove or not that.
    if lvl.is_tile_passable(posx + lookx, posy+looky) and lvl.is_tile_passable(posx + 2 * lookx, posy + 2 * looky):
        actor.move_forward()
        if actor.was_rotated_previous_turn:
            actor.was_rotated_previous_turn = False
            actor.prefers_clockwise_rotation = RND.rand_bool()
    else:
        actor.rotate_45_degrees(actor.prefers_clockwise_rotation)
        actor.was_rotated_previous_turn = True
