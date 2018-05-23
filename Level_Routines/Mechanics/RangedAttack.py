from ..Units.Unit import Unit
from Message_Log import MessageLog as LOG
from . import Damage as DMG
from Routines import SidavLOS as LOS


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
