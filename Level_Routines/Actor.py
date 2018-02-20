from .Unit import Unit
from enum import Enum


class Actor(Unit): # Not needed?

    states = Enum('states', 'calm distracted alerted engaging')
    current_state = None
    current_state_timeout = 0
    prefers_clockwise_rotation = True

    was_rotated_previous_turn = False # For AI.

    def __init__(self, x, y, appearance = '?'):
        super(Actor, self).__init__(x, y, appearance=appearance)
        self.current_state = self.states.calm

    def get_current_state(self):
        return self.current_state

    def set_current_state(self, state, timeout=0):
        self.current_state = state
        if timeout > 0:
            self.current_state_timeout = timeout

    def get_current_state_timeout(self):
        return self.current_state_timeout

    def set_current_state_timeout(self, timeout):
        self.current_state_timeout = timeout

    def decrease_current_state_timeout(self):
        if self.current_state_timeout > 0:
            self.current_state_timeout -= 1


    def get_appearance(self):
        if self.current_state == self.states.distracted:
            return '?'
        if self.current_state == self.states.alerted:
            return '!'
        return self._appearance
