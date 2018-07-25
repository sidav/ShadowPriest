from ..Units.Unit import Unit
from Message_Log import MessageLog as LOG
from ..Player import Statistics as stat

def do_damage_to_victim(damage, victim):
    victim.decrease_hitpoints(damage)
    if victim.get_current_hitpoints() <= 0 and not victim.is_of_type('Player'):
        stat.enemies_killed += 1
    elif victim.is_of_type('Player'):
        stat.total_hp_lost += damage
    LOG.append_warning_message('{} damage, {}\'s HP: {}/{}'.format(damage, victim.get_name(), victim.get_current_hitpoints(), victim.get_max_hitpoints()))
