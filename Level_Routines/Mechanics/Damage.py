from ..Units.Unit import Unit
from Message_Log import MessageLog as LOG
from ..Player import Statistics as stat

def do_damage_to_victim(damage, victim):
    if victim.get_current_hitpoints() <= 0 and not victim.is_of_type('Player'):
        stat.enemies_killed += 1
    victim.decrease_hitpoints(damage)
    LOG.append_warning_message('{} damage, {}\'s HP: {}/{}'.format(damage, victim.get_name(), victim.get_current_hitpoints(), victim.get_max_hitpoints()))
