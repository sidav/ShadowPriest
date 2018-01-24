from .Unit import Unit


class Player(Unit):

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, appearance='@')
        self._has_look_direction = False

