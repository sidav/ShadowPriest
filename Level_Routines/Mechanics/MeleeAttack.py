from ..Units.Unit import Unit
from Message_Log import MessageLog as LOG
from . import Damage as DMG


def try_to_stab(attacker:Unit, victim:Unit):
    if attacker.get_inventory().get_equipped_weapon() is None:
        LOG.append_warning_message('trying to stab with no weapon')
        return False
    attacker_weapon = attacker.get_inventory().get_equipped_weapon()
    attacker_stats = attacker.get_rpg_stats()
    damage = calculate_stab_damage(attacker_weapon.get_base_stab_damage(), attacker_stats)
    DMG.do_damage_to_victim(damage, victim)
    return True


def try_to_attack_with_bare_hands(attacker:Unit, victim:Unit):
    if attacker.get_inventory().get_equipped_weapon() is not None:
        LOG.append_error_message('bare-handed attack with weapon equipped')
        return False
    damage = calculate_barefist_damage(attacker.get_rpg_stats())
    DMG.do_damage_to_victim(damage, victim)
    return True


def try_to_attack_with_weapon(attacker:Unit, victim:Unit):
    attacker_weapon = attacker.get_inventory().get_equipped_weapon()
    attacker_stats = attacker.get_rpg_stats()
    damage = calculate_weapon_damage(attacker_weapon.get_base_melee_damage(), attacker_stats)
    DMG.do_damage_to_victim(damage, victim)
    return True


def calculate_barefist_damage(stats):
    # attacker.STR + attacker.NIM + attacker.fistfight_skill
    STR = stats.get_strength()
    NIM = stats.get_nimbleness()
    skill = stats.get_skill('fistfight')
    return STR + NIM + skill


def calculate_weapon_damage(base_dmg, stats):
    # (attacker.base_weapon_damage/5)*((attacker.STR + attacker.NIM)/2 + attacker.melee_weapon_skill)
    STR = stats.get_strength()
    NIM = stats.get_nimbleness()
    skill = stats.get_skill('melee')
    return (base_dmg // 5)*((STR + NIM) // 2) + skill


def calculate_stab_damage(base_stab_dmg, stats):
    stab_skill = stats.get_skill('stab')
    return int(base_stab_dmg * (1 + stab_skill / 100))
