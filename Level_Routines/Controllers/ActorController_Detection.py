from Routines import SidavAngularLOS as ALOS
from Routines import SidavLOS as LOS

# routine for checking NPC behaviour and something


def is_unit_seeing_position(lvl, actor, px, py):
    # vis_map = lvl.get_opacity_map()
    from_x, from_y = actor.get_position()
    fov_angle = actor.get_fov_angle()
    look_x, look_y = actor.get_look_direction()
    if (px - from_x) ** 2 + (py - from_y) ** 2 > actor.get_looking_range() ** 2:
        return False
    if not ALOS.is_point_in_sector(from_x, from_y, look_x, look_y, px, py, fov_angle):
        return False
    if not LOS._straightLOSCheck(from_x, from_y, px, py):  #TODO: WARNING: can cause seeing through closed doors or opposite behaviour. TODO: check that!
        return False
    return True


def is_actor_seeing_an_enemy(lvl, actor):
    # TODO: make detection of other enemies (using factions), not the player only.
    player = lvl.get_player()
    px, py = player.get_position()
    return is_unit_seeing_position(lvl, actor, px, py)


def get_list_of_seen_enemies(lvl, actor):
    # TODO: make detection of other enemies (using factions), not the player only.
    player = lvl.get_player()
    px, py = player.get_position()
    if is_unit_seeing_position(lvl, actor, px, py):
        return [player]
    else:
        return []