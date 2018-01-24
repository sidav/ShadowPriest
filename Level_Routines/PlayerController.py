from Routines import TdlConsoleWrapper as CW
# from .LevelModel import LevelModel


def do_key_action(lvl):
    player = lvl.get_player()
    px, py = player.get_position()
    keyPressed = CW.readKey()
    key = keyPressed.text
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
    if (lvl.is_tile_passable(px+vector_x, py+vector_y)):
        player.move_by_vector(vector_x, vector_y)