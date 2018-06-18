from enum import Enum

from ..Units.Unit import Unit


class Actor(Unit): # Not needed?

    ### AI data ###
    states = Enum('states', 'calm distracted alerted engaging')
    # current_state = None
    # current_state_expiration_turn = 0
    # target_unit = None  # for engaging or whatever
    # target_x = target_y = 0 # for "i must go here" behaviour
    # prefers_clockwise_rotation = True
    # was_rotated_previous_turn = False # For AI.
    ### /AI DATA ###

    def __init__(self, x, y, appearance = '?', color=(32, 192, 32), name='Unidentified Actor'):
        super(Actor, self).__init__(x, y, appearance=appearance, color=color, name=name)
        # AI DATA
        self.current_state = self.states.calm
        self.current_state_expiration_turn = 0
        self.was_rotated_previous_turn = False
        self.target_unit = None  # for engaging or whatever
        self.target_x = target_y = 0 # for "i must go here" behaviour
        self.prefers_clockwise_rotation = True
        self.was_rotated_previous_turn = False # For AI.
        # /AI DATA

    def set_target_coords(self, x, y):
        self.target_x, self.target_y = x, y

    def set_target_unit(self, unit):
        self.target_unit = unit

    def get_target_coords(self):
        return self.target_x, self.target_y

    def get_target_unit(self):
        return self.target_unit

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
