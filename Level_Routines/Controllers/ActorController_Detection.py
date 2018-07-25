from Routines import SidavAngularLOS as ALOS, SidavRandom as RAND, SidavLOS as LOS
from . import UnitController as UC
from Message_Log import MessageLog as LOG
from . import LevelController as LC
import math

# routine for checking NPC behaviour and something

# TODO: rewrite this whole file because this whole file is unneccessarily complicated bullshit.

def is_unit_seeing_position(lvl, actor, px, py):
    # vis_map = lvl.get_opacity_map()
    from_x, from_y = actor.get_position()
    fov_angle = actor.get_fov_angle()
    look_x, look_y = actor.get_look_direction()
    if (px - from_x) ** 2 + (py - from_y) ** 2 > UC.get_sight_range(actor) ** 2:
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
    state_doesnt_need_shadowcheck = actor.get_current_state() == actor.states.alerted
    return is_unit_seeing_position(lvl, actor, px, py) and (state_doesnt_need_shadowcheck or check_sight_with_shadow(actor, player))


def get_list_of_seen_enemies(lvl, actor):
    # TODO: make detection of other enemies (using factions), not the player only.
    player = lvl.get_player()
    px, py = player.get_position()
    if is_unit_seeing_position(lvl, actor, px, py):
        return [player]
    else:
        return []


def check_sight_with_shadow(seeing, target):
    if target.is_hidden_in_shadow():
        adv = seeing.get_rpg_stats().get_advertence()
        from_x, from_y = seeing.get_position()
        to_x, to_y = target.get_position()
        dist = math.sqrt((from_x - to_x) ** 2 + (from_y - to_y) ** 2)
        if dist <= 1.4:
            target.set_hidden_in_shadow(False)
            return True
        walls = LC.count_vision_blocking_tiles_around_coordinates(to_x, to_y)
        return _shadow_formula_check(walls, adv, dist)
    else:
        return True


def _shadow_formula_check(wall_score, adv, distance_to_target):
    percent = 10 * adv / ((wall_score) + distance_to_target // 2)  # SHADOWHIDE FORMULA HERE
    rand_check = RAND.rand(100)
    LOG.append_warning_message('W{} A{} D{:.1f}, FAIL_RISK {:.1f}, CHECK {} (player have been revealed: {})'.format(wall_score, adv, distance_to_target, percent, rand_check, rand_check < percent))
    return rand_check < percent
