from .. import LevelController as LC
from ..Units import TurnCosts as TC
from Routines import TdlConsoleWrapper as CW
from Message_Log import MessageLog as LOG

def do_grabbing(player):
    (x, y) = player.get_position()
    if LC.is_item_present(x, y):
        items_here = LC.get_items_at_coordinates(x, y)
        if len(items_here) == 1:
            if LC.try_pick_up_item(player, items_here[0]):
                player.spend_turns_for_action(TC.cost_for('pick up'))
                LOG.append_message('I pick up {}.'.format(items_here[0].get_name()))
            else:
                LOG.append_error_message("Can't pick up items here for unknown reason!")
        else:
            pass
    else:
        LOG.append_message("There is nothing here! ")


def pickup_menu(items):
    pass


def get_names_from_list_of_items(items):
    name_list = []
    for item in items:
        name_list.append(item.get_name())
    return name_list