from . import LevelTile


class DoorTile(LevelTile):
    closed = True

    def __init__(self):
        LevelTile.__init__()
        pass

    def get_tile_char(self):
        if self.closed:
            return '+'
        else:
            return '\\'
