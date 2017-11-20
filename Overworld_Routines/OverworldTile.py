
#represents one tile of the global map.
class OverworldTile:
    _appearance = '?'
    _color = None
    _passable = True;

    def __init__(self, appearance):
        self._appearance = appearance
