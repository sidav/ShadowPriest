from ..Units.Unit import Unit
from Message_Log import MessageLog as LOG


def try_to_attack(attacker:Unit, victim:Unit):
    attacker_weapon = attacker.get_inventory().get_equipped_weapon()
    attacker_stats = attacker.get_rpg_stats()

    damage = 0

    if attacker_weapon is None:
        damage = 15
    else:
        damage = calculate_weapon_damage(attacker_weapon.get_base_damage(), attacker_stats)
    do_damage(damage, victim)
    LOG.append_message('DBG: {} damage'.format(damage))


def do_damage(damage, victim):
    victim.decrease_hitpoints(damage)


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
