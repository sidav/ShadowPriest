from .. import LevelController as LC
from Level_Routines.Mechanics import TurnCosts as TC
from Message_Log import MessageLog as LOG
import SidavMenu as MENU


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
            pickup_with_pickup_menu(player, items_here)
    else:
        LOG.append_message("There is nothing here! ")


def do_dropping(player):
    inv = player.get_inventory()
    backpack = inv.get_backpack()
    if len(backpack) == 0:
        LOG.append_message('I have nothing to drop - my backpack is empty!')
        return
    names = get_names_from_list_of_items(backpack)
    indices = MENU.multi_select_menu('DROP ITEMS', 'Select items to drop',
                                     names)  # indices - indices of items selected
    items_to_drop = []
    for ind in indices:
        items_to_drop.append(backpack[ind])

    for item in items_to_drop:
        if LC.try_drop_item(player, item):
            player.spend_turns_for_action(TC.cost_for('drop item'))
            LOG.append_message('I drop {}.'.format(item.get_name()))
        else:
            LOG.append_error_message("Can't drop item for unknown reason!")


def do_wielding(player):
    inv = player.get_inventory()
    wpns = inv.get_weapons_from_backpack()
    if len(wpns) == 0:
        inv.unequip_weapon()
        return
    names = get_names_from_list_of_items(wpns)
    names.append('Nothing') # to unwield
    selected_weapon_index = MENU.single_select_menu('WIELD WEAPON', 'Select weapon to wield',
                                     names)
    if selected_weapon_index == len(names) - 1:  # player HAS selected nothing:
        inv.unequip_weapon()
    else:
        inv.equip_item(wpns[selected_weapon_index])


def do_unwielding(player):
    inv = player.get_inventory()
    inv.get_equipped_weapon()


def pickup_with_pickup_menu(player, items):
    names = get_names_from_list_of_items(items)
    indices = MENU.multi_select_menu('PICK UP', 'Select items to pick up', names) # indices - indices_of_items_selected_for_pickup
    for ind in indices:
        if LC.try_pick_up_item(player, items[ind]):
            player.spend_turns_for_action(TC.cost_for('pick up'))
            LOG.append_message('I pick up {}.'.format(items[ind].get_name()))
        else:
            LOG.append_error_message("Can't pick up items here for unknown reason!")


def show_equipped_items(player):
    inv = player.get_inventory()

    items_in_slots = [inv.get_equipped_weapon(), inv.get_equipped_armor(), inv.get_equipped_ammo()]

    item_slot_names = ['Weapon in hand', 'Equipped armor', 'Ammo in ready']
    items_in_slots_names = get_names_from_list_of_items(items_in_slots, 'Nothing')

    MENU.name_value_menu('INVENTORY', 'Look at my fucking inventory. Look. ', item_slot_names, items_in_slots_names)

def get_names_from_list_of_items(items, placeholder_for_empty='None_Item'):
    name_list = []
    for item in items:
        if item is not None:
            name_list.append(item.get_name())
        else:
            name_list.append(placeholder_for_empty)
    return name_list