from Message_Log import MessageLog as LOG
# Contains methods for calculation of lengths of actions (for the timing system)


def cost_for(action, unit=None):
    action = action.lower()
    if action == 'wait':
        return 10
    elif action == 'turn':
        return 7
    elif action == 'open door':
        return 15
    elif action == 'close door':
        return 12
    elif action == 'peek':
        return 10
    elif action == 'pick up':
        return 12
    elif action == 'drop item':
        return 10
    elif action == 'knockout attack':
        return 10
    elif action == 'lockpicking step':
        return 3

    # the next are the SNEAK-dependent time costs.
    if unit is None:
        LOG.append_error_message('No unit specified for "{0}" action.'.format(action))
        return 10
    str = unit.get_rpg_stats().get_strength()
    nim = unit.get_rpg_stats().get_nimbleness()
    end = unit.get_rpg_stats().get_endurance()
    adv = unit.get_rpg_stats().get_advertence()
    knw = unit.get_rpg_stats().get_knowledge()
    if action == 'move':
        if unit.is_of_type('Player'):
            return 10 - (nim // 3)
        return 10
    elif action == 'melee attack':
        return 16 - str // 2 - nim // 3
    elif action == 'firing':
        return 10
    elif action == 'quaffing':
        return 20 - end
    elif action == 'stab':
        return 25 - str - nim
    elif action == 'hide':
        return 15 - (adv + nim) // 2
    else:
        LOG.append_error_message('Time cost for unknown action "{0}" requested.'.format(action))
        return 10
