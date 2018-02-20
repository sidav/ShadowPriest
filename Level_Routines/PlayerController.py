from Routines import TdlConsoleWrapper as CW
from . import LevelView, LevelController
from Message_Log import MessageLog as LOG
# from .LevelModel import LevelModel


def do_key_action(lvl):

    player = lvl.get_player()

    if player.is_peeking():
        continue_peeking(player)
        return

    keyPressed = CW.readKey()
    key_text = keyPressed.text

    if not do_move_keys_action(lvl, player, key_text):
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


def do_move_keys_action(lvl, player, key):
    vector_x, vector_y = key_to_direction(key)
    if vector_x == vector_y == 0:
        return False
    px, py = player.get_position()

    if (lvl.is_tile_passable(px + vector_x, py + vector_y)):
        player.move_by_vector(vector_x, vector_y)
        player.spend_turns_for_action(9)
    elif lvl.is_door_present(px + vector_x, py + vector_y):
        LevelController.try_open_door(px + vector_x, py + vector_y)
        LOG.append_message("I open the door. ")
        player.spend_turns_for_action(15)
    return True


def try_close_door(lvl, player):
    px, py = player.get_position()
    to_x, to_y = ask_for_direction('Where to close a door?')
    if lvl.is_door_present(px+to_x, py+to_y):
        if LevelController.try_close_door(px+to_x, py+to_y):
            LOG.append_message("I close the door.")
        else:
            LOG.append_message("I can't close the door! ")
        player.spend_turns_for_action(12)
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
    player.spend_turns_for_action(5)


def continue_peeking(player):
    LOG.append_replaceable_message('I continue peeking... ')
    keyPressed = CW.readKey()
    if keyPressed.text != '5' and keyPressed.text != ' ':
        player.set_peeking(False)
        LOG.append_message('I recoil and look around. ')
    else:
        player.spend_turns_for_action(5)


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
