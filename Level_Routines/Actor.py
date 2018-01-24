from .Unit import Unit
from enum import Enum


class Actor(Unit): # Not needed?

    states = Enum('states', 'calm distracted alerted engaging')
    current_state = None

    def __init__(self, x, y, appearance = '?'):
        super(Actor, self).__init__(x, y, appearance=appearance)
        self.current_state = self.states.calm


