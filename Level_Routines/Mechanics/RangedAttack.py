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

    if not LOS._straightLOSCheck(a_x, a_y, v_x, v_y): # TODO: maybe use fullLOSLineCheck()?
        return False

    # TODO: check for enough ammo in clip
    # TODO: implement auto-firing guns

    attacker_stats = attacker.get_rpg_stats()
    damage = calculate_shooting_damage(attacker_weapon, attacker_stats)
    spend_ammo(attacker_weapon)
    DMG.do_damage_to_victim(damage, victim)
    return True


def calculate_shooting_damage(weapon, stats):
    return 10


def spend_ammo(weapon):
    return 10
