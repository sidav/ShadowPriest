from Routines import SidavAngularLOS as ALOS
from Routines import SidavLOS as LOS

# routine for checking NPC behaviour and something

def is_unit_seeing_position(lvl, actor, px, py):
    vis_map = lvl.get_opacity_map()
    from_x, from_y = actor.get_position()
    fov_angle = actor.get_fov_angle()
    look_x, look_y = actor.get_look_direction()
    if (px - from_x) ** 2 + (py - from_y) ** 2 > 6 ** 2:  # TODO: change range
        return False
    if not ALOS.is_point_in_sector(from_x, from_y, look_x, look_y, px, py, fov_angle):
        return False
    if not LOS._straightLOSCheck(from_x, from_y, px, py):
        return False
    return True
