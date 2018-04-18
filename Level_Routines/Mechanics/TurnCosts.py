from Message_Log import MessageLog as LOG
# Contains methods for calculation of lengths of actions (for the timing system)

def cost_for(action, unit=None):
    action = action.lower()
    if action == 'wait':
        return 10
    elif action == 'move':
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
    elif action == 'melee attack':
        return 10
    elif action == 'knockout attack':
        return 10

    else:
        LOG.append_error_message('Time cost for unknown action "{0}" requested.'.format(action))
        return 10
