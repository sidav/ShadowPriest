from enum import Enum

from ..Units.Unit import Unit


class Actor(Unit): # Not needed?

    states = Enum('states', 'calm distracted alerted engaging')
    current_state = None
    current_state_expiration_turn = 0
    prefers_clockwise_rotation = True

    was_rotated_previous_turn = False # For AI.

    def __init__(self, x, y, appearance = '?', color=(32, 192, 32), name='Unidentified Actor'):
        super(Actor, self).__init__(x, y, appearance=appearance, color=color, name=name)
        self.current_state = self.states.calm

    def get_current_state(self):
        return self.current_state

    def set_current_state(self, state, timeout=0):
        self.current_state = state
        if timeout > 0:
            self.current_state_expiration_turn = timeout

    # def check_current_state_expired(self):
    #     return self.current_state_expiration_turn <

    def can_be_stabbed(self):
        return self._stabbable and self.current_state == self.states.calm

    def get_current_state_expiration_turn(self):
        return self.current_state_expiration_turn

    def set_current_state_expiration_turn(self, timeout):
        self.current_state_expiration_turn += timeout

    def get_appearance(self):
        if self.current_state == self.states.distracted:
            return '?'
        if self.current_state == self.states.alerted:
            return '!'
        return self._appearance
