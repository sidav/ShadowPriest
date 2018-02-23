from .. import LevelController as LC
from ..Units import TurnCosts as TC
from Routines import TdlConsoleWrapper as CW
from Message_Log import MessageLog as LOG

def do_grabbing(player):
    (x, y) = player.get_position()
    if LC.is_item_present(x, y):
        pass
        # if LC.try_pick_up_item(player):
        #     player.spend_turns_for_action(TC.cost_for('pick up'))
    else:
        LOG.append_message("There is nothing here! ")


def pickup_menu(items):
    pass