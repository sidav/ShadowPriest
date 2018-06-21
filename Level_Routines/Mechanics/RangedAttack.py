from ..Units.Unit import Unit
from Message_Log import MessageLog as LOG
from . import Damage as DMG
from Routines import SidavLOS as LOS, TdlConsoleWrapper as CW
from ..Controllers import LevelController as LC


def try_to_shoot(attacker:Unit, victim:Unit):
    a_x, a_y = attacker.get_position()
    v_x, v_y = victim.get_position()
    attacker_weapon = attacker.get_inventory().get_equipped_weapon()
    if attacker_weapon is None or not attacker_weapon.is_of_type('RangedWeapon'):
        LOG.append_warning_message('trying to shoot with no ranged weapon')
        return False

    if not LOS._straightLOSCheck(a_x, a_y, v_x, v_y): # We use simpler method first to save calculation time...
        print('Using heavy LOS calculations!')
        vis_table = LOS.getVisibilityTableFromPosition(a_x, a_y) # ...and if that does not help, use heavy calculations.
        if not vis_table[v_x][v_y]:
            LOG.append_error_message('trying to shoot with no line of fire')
            return False

    # TODO: check for enough ammo in clip
    # TODO: implement auto-firing guns

    attacker_stats = attacker.get_rpg_stats()
    damage = calculate_shooting_damage(attacker_weapon, attacker_stats)
    spend_ammo(attacker_weapon)
    draw_bullet_trace(a_x, a_y, v_x, v_y, attacker_weapon.get_loaded_ammunition().get_color())
    DMG.do_damage_to_victim(damage, victim)
    return True


def calculate_shooting_damage(weapon, stats):
    return 35


def spend_ammo(weapon):
    # TODO: properly spend ammo for auto-firing guns
    if weapon.get_loaded_ammunition() is None:
        LOG.append_error_message('NoneType ammunition to spend!')
        return
    weapon.get_loaded_ammunition().change_quantity_by(-1)


# The next two methods maybe should be moved to some controller!


def draw_bullet_trace(fx, fy, tx, ty, color):
    from Routines import BresenhamLine as BL
    import time
    line = BL.get_line(fx, fy, tx, ty)
    bullet_char = get_bullet_char(fx, fy, tx, ty)
    for cell in line:
        LC.force_redraw_screen(False)
        # CW.setForegroundColor(color)
        CW.setForegroundColor(192, 192, 0)
        CW.putChar(bullet_char, cell.x, cell.y)
        CW.flushConsole()
        time.sleep(0.1)


def get_bullet_char(fx, fy, tx, ty):
    import math
    target_look_x = tx - fx
    target_look_y = ty - fy
    length = math.sqrt(target_look_x ** 2 + target_look_y ** 2)
    target_look_x /= length
    target_look_y /= length
    if abs(target_look_x) >= 0.5:
        target_look_x /= abs(target_look_x)
    else:
        target_look_x = 0
    if abs(target_look_y) >= 0.5:
        target_look_y /= abs(target_look_y)
    else:
        target_look_y = 0
    if target_look_x == 0:
        return '|'
    elif target_look_y == 0:
        return '-'
    elif target_look_x * target_look_y == 1:
        return '\\'
    elif target_look_x * target_look_y == -1:
        return '/'
    else:
        return '?'
