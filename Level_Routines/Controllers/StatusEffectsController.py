from . import LevelController as LC
from Message_Log import MessageLog as LOG

def apply_status_effects_to_a_unit(unit):
    all_se = unit.get_status_effects()
    for status_effect in all_se:
        if status_effect.get_name() == 'HEALING':
            unit.increase_hitpoints(1)
        elif status_effect.get_name() == 'POISON':
            unit.decrease_hitpoints(1)

        if status_effect.get_expiration_turn() < LC.get_current_turn():
            unit.remove_status_effect(status_effect)
        else:
            LOG.append_warning_message('Unknown status effect "{}" passed to a controller!'.format(status_effect.get_name()))
