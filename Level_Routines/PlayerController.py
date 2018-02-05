from Routines import TdlConsoleWrapper as CW
from . import LevelView
from Message_Log import MessageLog as LOG
# from .LevelModel import LevelModel


def do_key_action(lvl):
    keyPressed = CW.readKey()
    key_text = keyPressed.text
    player = lvl.get_player()
    if not do_move_keys_action(lvl, player, key_text):
        if key_text == '-':
            LevelView.SINGLE_ARROW_MODE ^= True # "some_bool ^= True" is equivalent to "some_bool = not some_bool"
            LOG.append_replaceable_message("Single arrow mode set to {0}".format(bool(LevelView.SINGLE_ARROW_MODE)))
        if keyPressed.key == 'F1':
            lvl.set_all_tiles_seen()
            LOG.append_replaceable_message('Set all tiles as seen. ')
        else:
            print("Not movement key!")


def do_move_keys_action(lvl, player, key):
    px, py = player.get_position()
    vector_x, vector_y = key_to_direction(key)
    if (lvl.is_tile_passable(px + vector_x, py + vector_y)):
        player.move_by_vector(vector_x, vector_y)
    if vector_x != 0 and vector_y != 0:
        return True
    else:
        return False


def ask_for_direction():
    LOG.append_replaceable_message('Pick a direction... ')
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
