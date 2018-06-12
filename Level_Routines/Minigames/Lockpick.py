from Routines import TdlConsoleWrapper as CW
from Routines import SidavRandom as random
from GLOBAL_DATA import Global_Constants as GC


class Lockpick:

    def __init__(self, pins, pin_positions):
        self._pins = pins
        self._pin_positions = pin_positions
        self._lockpick_coordinate = 0
        self._curr_pins_positions = []
        self._true_positions = []
        for i in range(pins):
            self._true_positions.append(random.rand(pin_positions))
            self._curr_pins_positions.append(pin_positions - 1)

    def draw_puzzle(self):
        puzzle_width = self._pins * 2 + 1
        puzzle_height = self._pin_positions + 2
        w_x = GC.CONSOLE_WIDTH // 2 - puzzle_width // 2
        w_y = GC.CONSOLE_HEIGHT // 2 - puzzle_height // 2
        for x in range(puzzle_width):
            for y in range(puzzle_height):
                CW.putChar(' ', x+w_x, y+w_y)
        for x in range(puzzle_width):
            if x % 2 == 0:
                # draw "walls":
                CW.setForegroundColor(64, 64, 64)
                for y in range(self._pin_positions):
                    CW.putChar(chr(177), x+w_x, y+w_y+1)
            else:
                # draw pins:
                CW.setForegroundColor(128, 128, 0)
                for y in range(self._curr_pins_positions[x // 2]):
                    CW.putChar('|', x+w_x, y+w_y+1)
                CW.putChar('V', x+w_x, w_y + self._curr_pins_positions[x // 2] + 1)

        # draw border:
        CW.setForegroundColor(64, 64, 64)
        for x in range(puzzle_width+1):
            for y in range(puzzle_height + 2):
                if x == 0 or x == puzzle_width or y == 0 or y == puzzle_height + 1:
                    CW.putString(chr(177), x + w_x, y + w_y)

        # draw lockpick:
        CW.setForegroundColor(32, 128, 128)
        for x in range(self._lockpick_coordinate * 2 + 1):
            CW.putChar('-', x + w_x, puzzle_height + w_y)
        CW.putChar('|', w_x + self._lockpick_coordinate * 2 + 1, puzzle_height + w_y)
        CW.putChar('|', w_x + self._lockpick_coordinate * 2 + 1, puzzle_height - 1 + w_y)

        CW.flushConsole()

    def do_turn(self, key):
        if key.text == '.' or key.text == '6':
            self._lockpick_coordinate += 1
            if self._lockpick_coordinate >= self._pins:
                self._lockpick_coordinate = 0
        elif key.text == ',' or key.text == '4':
            self._lockpick_coordinate -= 1
            if self._lockpick_coordinate < 0:
                self._lockpick_coordinate = self._pins - 1
        elif key.text == ' ' or key.text == '8':
            self._curr_pins_positions[self._lockpick_coordinate] -= 1
            if self._curr_pins_positions[self._lockpick_coordinate] < 0:
                self._curr_pins_positions[self._lockpick_coordinate] = self._pin_positions - 1
        #if key.keychar == 'ENTER':
        for i in range(self._pins):
            if self._curr_pins_positions[i] != self._true_positions[i]:
                return False
        return True
        # return False
