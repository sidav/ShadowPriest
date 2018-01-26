from Routines import TdlConsoleWrapper as CW
from . import LevelView
from Message_Log import MessageLog as LOG
# from .LevelModel import LevelModel


def do_key_action(lvl):
    keyPressed = CW.readKey()
    key = keyPressed.text
    player = lvl.get_player()
    if not do_move_keys_action(lvl, player, key):
        if key == '-':
            LevelView.SINGLE_ARROW_MODE ^= True # "some_bool ^= True" is equivalent to "some_bool = not some_bool"
            LOG.append_message("Single arrow mode set to {0}".format(bool(LevelView.SINGLE_ARROW_MODE)))
        else:
            print("Not movement key!")


def do_move_keys_action(lvl, player, key):
    px, py = player.get_position()
    vector_x = vector_y = 0
    if key == 'h':
        vector_x = -1
    elif key == 'j':
        vector_y = 1
    elif key == 'k':
        vector_y = -1
    elif key == 'l':
        vector_x = 1
    elif key == 'y':
        vector_x = -1
        vector_y = -1
    elif key == 'u':
        vector_x = 1
        vector_y = -1
    elif key == 'b':
        vector_x = -1
        vector_y = 1
    elif key == 'n':
        vector_x = 1
        vector_y = 1
    if (lvl.is_tile_passable(px + vector_x, py + vector_y)):
        player.move_by_vector(vector_x, vector_y)
    if vector_x != 0 and vector_y != 0:
        return True
    else:
        return False
