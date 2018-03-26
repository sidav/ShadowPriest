import Routines.SidavRandom as random
from .Inventory import Inventory

# Represents (as superclass) the player, some character or enemy or what the heck you want to.
class Unit:
    _name = 'Unidentified Unit'
    _max_hitpoints = 100
    _curr_hitpoints = _max_hitpoints
    _inventory = None
    _pos_x = _pos_y = 0
    _look_x = _look_y = 0
    _fov_angle = 110
    _has_look_direction = True # <-- is the "looking thingy" neccessary to draw?
    _looking_range = 6
    _appearance = 'G'
    _color = (32, 192, 32)
    _next_turn_to_act = 0

    def __init__(self, posx, posy, appearance = 'G', color=(32, 192, 32)):
        self._inventory = Inventory()
        self._appearance = appearance
        self._pos_x = posx
        self._pos_y = posy
        self._color = color
        while self._look_x == 0 and self._look_y == 0:
            self._look_x = random.rand(3) - 1
            self._look_y = random.rand(3) - 1
        pass

    def get_name(self):
        return self._name

    def move_forward(self):
        self._pos_x += self._look_x
        self._pos_y += self._look_y
        pass

    def move_by_vector(self, x, y):
        self._pos_x += x
        self._pos_y += y
        pass

    def rotate_90_degrees(self, clockwise=True):
        temp_x = self._look_x
        if clockwise:
            self._look_x = - self._look_y
            self._look_y = temp_x
        else:
            self._look_x = self._look_y
            self._look_y = - temp_x

    def rotate_45_degrees(self, clockwise=True):
        temp_x = self._look_x
        if clockwise:
            self._look_x += - self._look_y
            self._look_y += temp_x
        else:
            self._look_x += self._look_y
            self._look_y += - temp_x

        if self._look_x != 0:
            self._look_x //= abs(self._look_x)
        if self._look_y != 0:
            self._look_y //= abs(self._look_y)

    def spend_turns_for_action(self, turns):
        self._next_turn_to_act += turns

    def get_next_turn_to_act(self):
        return self._next_turn_to_act

    def has_look_direction(self):
        return self._has_look_direction

    def get_position(self):
        return self._pos_x, self._pos_y

    def get_look_direction(self):
        return self._look_x, self._look_y

    def get_appearance(self):
        return self._appearance

    def get_color(self):
        return self._color

    def get_fov_angle(self):
        return self._fov_angle

    def get_looking_range(self):
        return self._looking_range

    def get_max_hitpoints(self):
        return self._max_hitpoints

    def get_current_hitpoints(self):
        return self._curr_hitpoints

    def decrease_hitpoints(self, dmg):
        self._curr_hitpoints -= dmg

    def is_dead(self):
        return self._curr_hitpoints <= 0

    def get_inventory(self):
        return self._inventory
1