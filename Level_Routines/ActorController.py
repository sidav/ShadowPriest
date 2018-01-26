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
    if lvl.is_tile_passable(posx + lookx, posy+looky):
        actor.move_forward()
        if actor.nameme:
            actor.nameme = False
            actor.prefers_clockwise_rotation = bool(RND.rand(2))
    else:
        actor.rotate_45_degrees(actor.prefers_clockwise_rotation)
        actor.nameme = True
