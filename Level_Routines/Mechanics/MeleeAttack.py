from ..Units.Unit import Unit


def do_attack(attacker:Unit, victim:Unit):
    attacker_weapon = attacker.get_inventory().get_equipped_weapon()
    damage = 0

    if attacker_weapon is None:
        damage = 15
    else:
        damage = 25
    do_damage(damage, victim)


def do_damage(damage, victim):
    victim.decrease_hitpoints(damage)
