from ..Units.Unit import Unit
from Message_Log import MessageLog as LOG

def do_damage_to_victim(damage, victim):
    victim.decrease_hitpoints(damage)
    LOG.append_warning_message('{} damage, {}\'s HP: {}/{}'.format(damage, victim.get_name(), victim.get_current_hitpoints(), victim.get_max_hitpoints()))
