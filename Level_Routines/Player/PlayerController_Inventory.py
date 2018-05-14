from .. import LevelController as LC
from Level_Routines.Mechanics import TurnCosts as TC
from Message_Log import MessageLog as LOG
import SidavMenu as MENU


def do_grabbing(player):
    inv = player.get_inventory()
    if inv.is_carrying_body_on_shoulder():
        LOG.append_message("I can't pick up with that burden on my shoulder.")
        return

    (x, y) = player.get_position()
    if LC.is_item_present(x, y):
        items_here = LC.get_items_at_coordinates(x, y)
        if len(items_here) == 1:
            if LC.try_pick_up_item(player, items_here[0]):
                player.spend_turns_for_action(TC.cost_for('pick up'))
                LOG.append_message(pick_up_message_for_item(items_here[0]))
            else:
                LOG.append_error_message("Can't pick up items here for unknown reason!")
        else:
            pickup_with_pickup_menu(player, items_here)
    else:
        LOG.append_message("There is nothing here! ")


def do_dropping(player):
    inv = player.get_inventory()
    backpack = inv.get_backpack()

    if inv.is_carrying_body_on_shoulder():
        body = inv.get_body_on_shoulder()
        if LC.try_drop_item(player, body):
            player.spend_turns_for_action(TC.cost_for('drop item'))
            LOG.append_message('I throw off the {} from my shoulder.'.format(body.get_name()))
            player.spend_turns_for_action(TC.cost_for('drop item'))
            return

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
            LOG.append_message('I drop the {}.'.format(item.get_name()))
        else:
            LOG.append_error_message("Can't drop item for unknown reason!")


def do_wielding(player):
    inv = player.get_inventory()

    if inv.is_carrying_body_on_shoulder():
        LOG.append_message("I can't change weapon with that burden on my shoulder.")
        return

    curr_weapon = inv.get_equipped_weapon()
    wpns = inv.get_weapons_from_backpack()
    if len(wpns) == 0:
        if curr_weapon is not None:
            LOG.append_message('I unwield my {}.'.format(inv.get_equipped_weapon().get_name()))
            inv.move_weapon_to_backpack()
        else:
            LOG.append_message('I have nothing to wield!')

    elif len(wpns) == 1 and curr_weapon is None:
        LOG.append_message('I wield the {}.'.format(wpns[0].get_name()))
        inv.equip_item(wpns[0])

    else:
        names = get_names_from_list_of_items(wpns)
        names.append('Nothing')  # for unwielding
        selected_weapon_index = MENU.single_select_menu('WIELD WEAPON', 'Select weapon to wield',
                                         names)
        if selected_weapon_index is None:
            LOG.append_replaceable_message('Okay, then.')
        else:
            if selected_weapon_index == len(names) - 1:  # player HAS selected nothing:
                if curr_weapon is not None:
                    LOG.append_message('I unwield my {}.'.format(inv.get_equipped_weapon().get_name()))
                    inv.move_weapon_to_backpack()
                else:
                    LOG.append_message('I decided to remain barehanded.')
            else:
                LOG.append_message('I wield the {}.'.format(wpns[0].get_name()))
                inv.equip_item(wpns[selected_weapon_index])


def do_quivering(player):
    inv = player.get_inventory()

    if inv.is_carrying_body_on_shoulder():
        LOG.append_message("I can't ready ammo with that burden on my shoulder.")
        return

    # curr_ammo = inv.get_equipped_ammo()
    ammo = inv.get_ammunition_from_backpack()
    if len(ammo) == 0:
        LOG.append_message('I have nothing to ready!')

    elif len(ammo) == 1:
        LOG.append_message('I ready the {}.'.format(ammo[0].get_name()))
        inv.equip_item(ammo[0])

    else:
        names = get_names_from_list_of_items(ammo)
        selected_ammo_index = MENU.single_select_menu('READY AMMO', 'Select  ammunition to ready',
                                         names)
        if selected_ammo_index is None:
            LOG.append_replaceable_message('Okay, then.')
        else:
            LOG.append_message('I ready the {}.'.format(ammo[0].get_name()))
            inv.equip_item(ammo[selected_ammo_index])


# def do_unwielding(player):
#     inv = player.get_inventory()
#     inv.get_equipped_weapon()


def pickup_with_pickup_menu(player, items):
    names = get_names_from_list_of_items(items)
    indices = MENU.multi_select_menu('PICK UP', 'Select items to pick up', names) # indices - indices_of_items_selected_for_pickup
    for ind in indices:
        if LC.try_pick_up_item(player, items[ind]):
            player.spend_turns_for_action(TC.cost_for('pick up'))
            LOG.append_message(pick_up_message_for_item(items[ind]))
        else:
            LOG.append_error_message("Can't pick up items here for unknown reason!")


def show_equipped_items(player):
    inv = player.get_inventory()
    backpack = inv.get_backpack()

    items_in_slots = [inv.get_equipped_weapon(), inv.get_equipped_armor(), inv.get_equipped_ammo()]

    item_slot_names = ['Weapon in hand', 'Equipped armor', 'Ammo in ready']
    items_in_slots_names = get_names_from_list_of_items(items_in_slots, 'Nothing')

    if inv.is_carrying_body_on_shoulder():
        item_slot_names = ['Body on shoulder'] + item_slot_names
        items_in_slots_names = [inv.get_body_on_shoulder().get_name()] + items_in_slots_names

    item_slot_names.append('')
    items_in_slots_names.append('')

    item_slot_names.append('-------- Backpack')
    if len(backpack) > 0:
        items_in_slots_names.append('')
    else:
        items_in_slots_names.append('empty')

    for item in backpack:
        item_slot_names.append('')
        items_in_slots_names.append(item.get_name())

    MENU.name_value_menu('INVENTORY', 'My items', item_slot_names, items_in_slots_names)


def get_names_from_list_of_items(items, placeholder_for_empty='None_Item'):
    name_list = []
    for item in items:
        if item is not None:
            name_list.append(item.get_name())
        else:
            name_list.append(placeholder_for_empty)
    return name_list


def pick_up_message_for_item(item):
    if item.is_body():
        return 'I shoulder the {}.'.format(item.get_name())
    else:
        return 'I pick up the {}.'.format(item.get_name())
