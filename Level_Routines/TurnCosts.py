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

    else:
        LOG.append_error_message('Unknown action "{0}" executed'.format(action))
        return 1