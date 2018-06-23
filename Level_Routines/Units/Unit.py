import math
import Routines.SidavRandom as random
from .Inventory import Inventory
from ..Mechanics.Sneak import RpgStats

# Represents (as superclass) the player, some character or enemy or what the heck you want to.
class Unit:
    _name = 'Unidentified Unit'
    _max_hitpoints = 100
    _curr_hitpoints = _max_hitpoints
    _faction = 1  # 0 is player's faction.

    _inventory = None
    _pos_x = _pos_y = 0
    _look_x = _look_y = 0
    _fov_angle = 110
    _has_look_direction = True # <-- is the "looking thingy" neccessary to draw?
    _looking_range = 6
    _appearance = 'G'
    _color = (32, 192, 32)
    _next_turn_to_act = 0

    _stabbable = True

    def __init__(self, posx, posy, appearance = 'G', color=(32, 192, 32), name='Unidentified Unit', rpg_stats = None):
        self._inventory = Inventory()
        self._appearance = appearance
        self._pos_x = posx
        self._pos_y = posy
        self._color = color
        self._name = name
        self.rpg_stats = RpgStats()
        self._status_effects = []
        if rpg_stats != None:
            self.rpg_stats = rpg_stats
        while self._look_x == 0 and self._look_y == 0:
            self._look_x = random.rand(3) - 1
            self._look_y = random.rand(3) - 1


    def set_coordinates(self, x, y):
        self._pos_x = x
        self._pos_y = y

    def set_next_turn_to_act(self, tick):
        self._next_turn_to_act = tick

    def can_be_stabbed(self):
        return self._stabbable

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def move_forward(self):
        self._pos_x += self._look_x
        self._pos_y += self._look_y
        pass

    def move_by_vector(self, x, y):
        self._pos_x += x
        self._pos_y += y
        pass

    def set_look_direction(self, x, y):
        self._look_x, self._look_y = x, y

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

    def look_at_coordinates(self, x, y):
        target_look_x = x - self._pos_x
        target_look_y = y - self._pos_y
        length = math.sqrt(target_look_x ** 2 + target_look_y ** 2)
        target_look_x /= length
        target_look_y /= length
        if abs(target_look_x) >= 0.5:
            target_look_x /= abs(target_look_x)
        else:
            target_look_x = 0
        if abs(target_look_y) >= 0.5:
            target_look_y /= abs(target_look_y)
        else:
            target_look_y = 0
        self.set_look_direction(target_look_x, target_look_y)

    def get_faction(self):
        return self._faction

    def get_rpg_stats(self):
        return self.rpg_stats

    def get_status_effects(self):
        return self._status_effects

    def count_status_effect(self, effect_name):
        count = 0
        for effect in self._status_effects:
            if effect.get_name() == effect_name:
                count += 1
        return count

    def add_status_effect(self, status_effect):
        self._status_effects.append(status_effect)

    def remove_status_effect(self, status_effect):
        self._status_effects.remove(status_effect)

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
        if self._curr_hitpoints < 0:
            self._curr_hitpoints = 0

    def increase_hitpoints(self, inc):
        self._curr_hitpoints += inc
        if self._curr_hitpoints > self._max_hitpoints:
            self._curr_hitpoints = self._max_hitpoints

    def is_player(self):
        return False

    def is_dead(self):
        return self._curr_hitpoints <= 0

    def get_inventory(self):
        return self._inventory

    def is_of_type(self, type):
        return self.__class__.__name__ == type
