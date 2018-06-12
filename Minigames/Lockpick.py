from Routines import TdlConsoleWrapper as CW
from Routines import SidavRandom as random


class Lockpick:
    true_positions = []
    pins = 2
    pin_positions = 3
    lockpick_coordinate = 0
    curr_pins_positions = []

    def __init__(self, pins = 2, pin_positions = 3):
        self.pins = pins
        self.pin_positions = pin_positions
        for i in range(pins):
            self.true_positions.append(random.rand(pin_positions))
            self.curr_pins_positions.append(pin_positions - 1)

    def draw_puzzle(self, w_x, w_y):
        puzzle_width = self.pins * 2 + 1
        puzzle_height = self.pin_positions + 2
        for x in range(puzzle_width):
            if x % 2 == 0:
                # draw "walls":
                CW.setForegroundColor(64, 64, 64)
                for y in range(self.pin_positions):
                    CW.putChar(chr(177), x+w_x, y+w_y+1)
            else:
                # draw pins:
                CW.setForegroundColor(128, 128, 0)
                for y in range(self.curr_pins_positions[x // 2]):
                    CW.putChar('|', x+w_x, y+w_y+1)
                CW.putChar('V', x+w_x, w_y + self.curr_pins_positions[x // 2] + 1)

        # draw border:
        CW.setForegroundColor(64, 64, 64)
        for x in range(puzzle_width+1):
            for y in range(puzzle_height + 2):
                if x == 0 or x == puzzle_width or y == 0 or y == puzzle_height + 1:
                    CW.putString(chr(177), x + w_x, y + w_y)

        # draw lockpick:
        CW.setForegroundColor(32, 128, 128)
        for x in range(self.lockpick_coordinate * 2 + 1):
            CW.putChar('-', x + w_x, puzzle_height + w_y)
        CW.putChar('|', w_x + self.lockpick_coordinate * 2 + 1, puzzle_height + w_y)
        CW.putChar('|', w_x + self.lockpick_coordinate * 2 + 1, puzzle_height - 1 + w_y)

    def do_turn(self):
        key = CW.readKey()
        if key.text == '.':
            self.lockpick_coordinate += 1
            if self.lockpick_coordinate >= self.pins:
                self.lockpick_coordinate = 0
        elif key.text == ',':
            self.lockpick_coordinate-=1
            if self.lockpick_coordinate < 0:
                self.lockpick_coordinate = self.pins - 1
        elif key.text == ' ':
            self.curr_pins_positions[self.lockpick_coordinate] -= 1
            if self.curr_pins_positions[self.lockpick_coordinate] < 0:
                self.curr_pins_positions[self.lockpick_coordinate] = self.pin_positions - 1
        #if key.keychar == 'ENTER':
        for i in range(self.pins):
            if self.curr_pins_positions[i] != self.true_positions[i]:
                return False
        return True
        return False
