from .Unit import Unit


class Actor(Unit): # Not needed?

    def __init__(self, x, y, appearance = '?'):
        super(Actor, self).__init__(x, y, appearance=appearance)


