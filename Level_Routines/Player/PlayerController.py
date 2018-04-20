from Level_Routines import LevelView, LevelController as LC
from Level_Routines.Mechanics import TurnCosts as TC
from Message_Log import MessageLog as LOG
from Routines import TdlConsoleWrapper as CW
from . import PlayerController_Inventory as PC_I
from ..LevelModel import LevelModel


def do_key_action(lvl):

    player = lvl.get_player()

    if player.is_peeking():
        continue_peeking(player)
        return

    keyPressed = CW.readKey()
    key_text = keyPressed.text

    if not do_move_keys_action(lvl, player, key_text):
        if keyPressed.text == '5' or keyPressed.text == ' ':
            player.spend_turns_for_action(TC.cost_for('wait'))
            LOG.append_message('I wait for a sec. ')
        if key_text == '-':
            LevelView.SINGLE_ARROW_MODE ^= True # "some_bool ^= True" is equivalent to "some_bool = not some_bool"
            LOG.append_replaceable_message("Single arrow mode set to {0}".format(bool(LevelView.SINGLE_ARROW_MODE)))
        if keyPressed.key == 'F1': # debug: magic mapping
            lvl.set_all_tiles_seen()
            LOG.append_replaceable_message('Set all tiles as seen. ')
        if keyPressed.text == 'c': # close door
            try_close_door(lvl, player)
        if keyPressed.text == 'p': # peek
            do_peeking(lvl, player)
        if keyPressed.text == 's': # strangle
            do_ko_attack(lvl, player)
        if keyPressed.text == 'g': # grab
            PC_I.do_grabbing(player)
        if keyPressed.text == 'G': # lay out items from body
            do_body_searching(player)
        if keyPressed.text == 'd': # drop
            PC_I.do_dropping(player)
        if keyPressed.text == 'w': # wield
            PC_I.do_wielding(player)
        if keyPressed.text == 'U': # unwield
            PC_I.do_unwielding(player)
        if keyPressed.text == 'i': # list equipped items
            PC_I.show_equipped_items(player)


def do_move_keys_action(lvl, player, key):
    vector_x, vector_y = key_to_direction(key)
    if vector_x == vector_y == 0:
        return False
    px, py = player.get_position()
    target_x, target_y = px + vector_x, py + vector_y

    if lvl.is_unit_present(target_x, target_y):
        target_unit = lvl.get_unit_at(target_x, target_y)
        LC.melee_attack(player, target_unit)
        player.spend_turns_for_action(TC.cost_for('melee attack'))
    elif (lvl.is_tile_passable(target_x, target_y)):
        player.move_by_vector(vector_x, vector_y)
        player.spend_turns_for_action(TC.cost_for('move'))
        notify_for_items_on_floor(player)
    elif lvl.is_door_present(target_x, target_y):
        LC.try_open_door(player, target_x, target_y)
        player.spend_turns_for_action(TC.cost_for('open door'))
    return True


def try_close_door(lvl, player):
    px, py = player.get_position()
    to_x, to_y = ask_for_direction('Where to close a door?')
    if lvl.is_door_present(px+to_x, py+to_y):
        if LC.try_close_door(player, px+to_x, py+to_y):
            pass
        else:
            LOG.append_message("I can't close the door! ")
        player.spend_turns_for_action(TC.cost_for('close door'))
    else:
        LOG.append_message('There is no door here!')


def do_peeking(lvl, player):
    px, py = player.get_position()
    peek_x, peek_y = ask_for_direction('Peek in which direction?')
    if not (lvl.is_door_present(px + peek_x, py + peek_y) or lvl.is_tile_passable(px + peek_x, py + peek_y)):
        LOG.append_message("I can't peek there! ")
        return
    player.set_peeking(True)
    player.set_peeking_vector(peek_x, peek_y)
    LOG.append_message('I carefully peek there... ')
    LOG.append_replaceable_message('I can pass turns with space or 5 to continue peeking.')
    player.spend_turns_for_action(TC.cost_for('peek'))


def continue_peeking(player):
    LOG.append_replaceable_message('I continue peeking... ')
    keyPressed = CW.readKey()
    if keyPressed.text != '5' and keyPressed.text != ' ':
        player.set_peeking(False)
        LOG.append_message('I recoil and look around. ')
    else:
        player.spend_turns_for_action(TC.cost_for('peek'))


def notify_for_items_on_floor(player):
    px, py = player.get_position()
    if LC.is_item_present(px, py):
        item_message = 'I see here: '
        items_here = LC.get_items_at_coordinates(px, py)
        item_message += items_here[0].get_name()
        if len(items_here) > 1:
            item_message += ' and {} more items'.format(len(items_here)-1)
        item_message += '.'
        LOG.append_message(item_message)


def do_ko_attack(lvl, player):
    px, py = player.get_position()
    grab_x, grab_y = ask_for_direction('Grab whom?')
    if grab_x == 0 and grab_y == 0:
        LOG.append_message("I don't find it funny.")
        return 
    target_x = px + grab_x
    target_y = py + grab_y
    if lvl.is_unit_present(target_x, target_y):
        target_unit = lvl.get_unit_at(target_x, target_y)
        LC.knockout_attack(player, target_unit)
        player.spend_turns_for_action(TC.cost_for('knockout attack'))
    else:
        LOG.append_message('There is nobody here!')


def do_body_searching(player):
    x, y = player.get_position()
    if LC.is_body_present_at(x, y):
        if LC.try_lay_out_items_from_body(player):
            LOG.append_message("I've laid out items from the body on floor.")
        else:
            LOG.append_message("I've already searched everything here.")
    else:
        LOG.append_message('There are no bodies here!')


##########################################################
def ask_for_direction(log_text='Pick a direction...'):
    LOG.append_replaceable_message(log_text)
    keyPressed = CW.readKey()
    return key_to_direction(keyPressed.text)


def key_to_direction(key):
    vector_x = vector_y = 0
    if key == 'h' or key == '4':
        vector_x = -1
    elif key == 'j' or key == '2':
        vector_y = 1
    elif key == 'k' or key == '8':
        vector_y = -1
    elif key == 'l' or key == '6':
        vector_x = 1
    elif key == 'y' or key == '7':
        vector_x = -1
        vector_y = -1
    elif key == 'u' or key == '9':
        vector_x = 1
        vector_y = -1
    elif key == 'b' or key == '1':
        vector_x = -1
        vector_y = 1
    elif key == 'n' or key == '3':
        vector_x = 1
        vector_y = 1
    return vector_x, vector_y
