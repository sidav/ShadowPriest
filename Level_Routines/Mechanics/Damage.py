from ..Units.Unit import Unit
from Message_Log import MessageLog as LOG

def do_damage_to_victim(damage, victim):
    victim.decrease_hitpoints(damage)
    LOG.append_message('DBG: {} damage'.format(damage))
