from ..Units.Unit import Unit


class Player(Unit):

    _is_peeking = False
    _peek_x = _peek_y = 0

    def __init__(self, x, y):
        super(Player, self).__init__(x, y, appearance='@')
        self._has_look_direction = False
        self._looking_range = 8

    def is_peeking(self):
        return self._is_peeking

    def set_peeking(self, b):
        self._is_peeking = b

    def set_peeking_vector(self, x, y):
        self._peek_x = x
        self._peek_y = y

    def get_peeking_vector(self):
        return self._peek_x, self._peek_y
