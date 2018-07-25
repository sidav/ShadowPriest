from . import LevelController as LC
from Message_Log import MessageLog as LOG
from ..Mechanics.StatusEffect import StatusEffect
from ..Player import Statistics as stat


PAINKILLER_HEALING_AMOUNT = 50 # TODO: move this somewhere!


def add_potion_status_effect_to_a_unit(potion, unit):
    se_name = potion.get_status_effect_name()
    se_expiration_turn = LC.get_current_turn() + potion.get_status_effect_duration()

    if se_name == 'PAINKILLER':
        if unit.get_current_hitpoints()+PAINKILLER_HEALING_AMOUNT > unit.get_max_hitpoints():
            se_expiration_turn = LC.get_current_turn() + 10 * ((unit.get_max_hitpoints() - unit.get_current_hitpoints()) // 2) # TODO: deconstantize that crap
        unit.increase_hitpoints(PAINKILLER_HEALING_AMOUNT)
        if unit.is_of_type('Player'):
            stat.total_healed += LC.get_current_turn() - 10 * ((unit.get_max_hitpoints() - unit.get_current_hitpoints()) // 2)

    # apply_specific_status_effect_to_a_unit(se_name, unit)
    unit.add_status_effect(StatusEffect(se_name, se_expiration_turn))


def apply_all_status_effects_to_a_unit(unit):
    all_se = unit.get_status_effects()
    for status_effect in all_se:
        se_name = status_effect.get_name()
        if status_effect.get_expiration_turn() <= LC.get_current_turn():
            unit.remove_status_effect(status_effect)
        apply_specific_status_effect_to_a_unit(se_name, unit)


def apply_specific_status_effect_to_a_unit(se_name, unit):
    if se_name == 'HEALING':
        unit.increase_hitpoints(1)
        if unit.is_of_type('Player'):
            stat.total_healed += 1
    elif se_name == 'POISON':
        unit.decrease_hitpoints(1)
        if unit.is_of_type('Player'):
            stat.total_hp_lost += 1
    elif se_name == 'PAINKILLER':
        unit.decrease_hitpoints(2)
        if unit.is_of_type('Player'):
            stat.total_hp_lost += 2
    else:
        LOG.append_warning_message('Unknown status effect "{}" passed to a controller!'.format(se_name))
