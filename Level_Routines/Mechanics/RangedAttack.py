from ..Units.Unit import Unit
from Message_Log import MessageLog as LOG
from . import Damage as DMG


def try_to_shoot(attacker:Unit, victim:Unit):
    if attacker.get_inventory().get_equipped_weapon() is None:
        LOG.append_warning_message('trying to stab with no weapon')
        return False
    attacker_weapon = attacker.get_inventory().get_equipped_weapon()
    attacker_stats = attacker.get_rpg_stats()
    damage = calculate_stab_damage(attacker_weapon.get_base_stab_damage(), attacker_stats)
    DMG.do_damage_to_victim(damage, victim)
    return True
