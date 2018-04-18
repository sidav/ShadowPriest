from ..Units.Unit import Unit
from Message_Log import MessageLog as LOG


def try_to_knockout(attacker:Unit, victim:Unit):
    # if attacker.get_inventory().get_equipped_weapon() is not None:
    #     LOG.append_warning_message('trying to strangle with weapon in hands!')
    return True


def calculate_knockout_time(attacker:Unit, victim:Unit):
    attacker_stats = attacker.get_rpg_stats()
    knockout_time = 100
    return knockout_time
