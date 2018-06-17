from Routines import TdlConsoleWrapper as CW
from GLOBAL_DATA import Global_Constants as GC
import Decorations as DECOR

C_W, C_H = GC.CONSOLE_WIDTH, GC.CONSOLE_HEIGHT
# cursor_line = 0

def _draw_titlebar(title, fgcolor=(128, 128, 128), bgcolor=(128, 0, 0)):
    CW.setBackgroundColor(bgcolor)
    CW.setForegroundColor(0, 0, 0)
    for i in range(C_W):
        CW.putChar(' ', i, 0)
    title = ' '+title+' '
    title_width = len(title)
    title_xcoord = (C_W // 2) - (title_width // 2) - 1
    CW.setBackgroundColor(0, 0, 0)
    CW.setForegroundColor(bgcolor)
    CW.putString(title, title_xcoord, 0)


def _draw_line_at_the_bottom(text):
    CW.setBackgroundColor(0, 0, 0)
    CW.setForegroundColor(192, 192, 192)
    CW.putString(text, 0, C_H-1)

def draw_title_and_subheading(title, subheading, subheading_upper_margin = 1, center_subheading = False):
    subheading_margin = C_W // 2 - len(subheading) // 2 if center_subheading else 0
    CW.clearConsole()
    color = (128, 128, 128)
    _draw_titlebar(title)
    CW.setForegroundColor(color)
    CW.putString(subheading, subheading_margin, subheading_upper_margin)


def name_value_menu(title='Name-value menu. Pick a title, dummy!', subheading='Pick subheading, dummy!',
                    names = [], values=[]):  # for inventory and whatever
    # cursor_line = 0
    # items_in_menu = len(items)

    draw_title_and_subheading(title, subheading)
    names_color = (192, 192, 192)
    values_color = (128, 128, 128)

    width_of_name_column = 0
    for name in names:
        if len(name) >= width_of_name_column:
            width_of_name_column = len(name) + 3

    CW.setForegroundColor(names_color)
    for i, name in enumerate(names):
        if name != '':
            CW.putString(name+':  ', 0, i+2)

    CW.setForegroundColor(values_color)
    for i, value in enumerate(values):
        CW.putString(str(value), width_of_name_column+2, i + 2)

    CW.flushConsole()

    while 1:
        key = CW.readKey()
        if key.keychar.__contains__('ENTER') or key.keychar == 'ESCAPE' or key.text == ' ':
            return




def single_select_menu(title='Single Select. Pick a title, dummy!', subheading='Pick subheading, dummy!', items=[]):
    cursor_line = 0
    color = (128, 128, 128)
    items_in_menu = len(items)

    draw_title_and_subheading(title, subheading)

    while 1:
        for i, item in enumerate(items):
            if (i == cursor_line):
                CW.setForegroundColor(0, 0, 0)
                CW.setBackgroundColor(color)
            else:
                CW.setForegroundColor(color)
                CW.setBackgroundColor(0, 0, 0)
            CW.putString(' '+item+' ', 0, 2+i)
        CW.setBackgroundColor(0, 0, 0)
        CW.flushConsole()

        key = CW.readKey()
        if key.keychar == 'DOWN' or key.text == '2':
            cursor_line += 1
            if cursor_line >= items_in_menu:
                cursor_line = 0
        elif key.keychar == 'UP' or key.text == '8':
            cursor_line -= 1
            if cursor_line < 0:
                cursor_line = items_in_menu - 1
        elif key.keychar.__contains__('ENTER') or key.text == ' ':
            return cursor_line
        elif key.keychar == 'ESCAPE':
            return None


def multi_select_menu(title='Multi Select. Pick a title, dummy!', subheading='Pick subheading, dummy!', items=[]):
    # returns the list of indexes of selected values.
    cursor_line = 0
    color = (128, 128, 128)
    items_in_menu = len(items)
    selected_items = [False for _ in range(items_in_menu)]

    draw_title_and_subheading(title, subheading)

    _draw_line_at_the_bottom('SPACE: select at the cursor, a/d: select/deselect all, ENTER: confirm selected')

    while 1:
        for i, item in enumerate(items):
            if (i == cursor_line):
                CW.setForegroundColor(0, 0, 0)
                CW.setBackgroundColor(color)
            else:
                CW.setForegroundColor(color)
                CW.setBackgroundColor(0, 0, 0)
            if selected_items[i]:
                CW.putString(' + ' + item + ' +', 0, 2 + i)
            else:
                CW.putString(' ' + item + '    ', 0, 2+i)
        CW.setBackgroundColor(0, 0, 0)
        CW.flushConsole()

        key = CW.readKey()
        if key.keychar == 'DOWN' or key.text == '2':
            cursor_line += 1
            if cursor_line >= items_in_menu:
                cursor_line = 0
        elif key.keychar == 'UP' or key.text == '8':
            cursor_line -= 1
            if cursor_line < 0:
                cursor_line = items_in_menu - 1
        elif key.text == 'a':
            for i in range(items_in_menu):
                selected_items[i] = 1
        elif key.text == 'd':
            for i in range(items_in_menu):
                selected_items[i] = 0
        elif key.text == ' ':
            selected_items[cursor_line] ^= 1
        elif key.keychar.__contains__('ENTER'):
            # form a list of indices
            result = []
            for i, bool in enumerate(selected_items):
                if bool:
                    result.append(i)
            return result
        elif key.keychar == 'ESCAPE':
            # cancel selection
            return []


def values_pick_menu(title, subheading, names, descriptions,
                     min_permitted_value=0, max_permitted_value=10, min_sum_of_values = 0, max_sum_of_values=10):
    # returns the list of values of selected lines.
    cursor_line = 0
    items_in_menu = len(names)
    values = [min_permitted_value for _ in range(len(names))]
    names_color = (164, 164, 164)
    descriptions_color = (64, 32, 128)

    left_arrow = '< '
    left_arrow_denied = '  '
    right_arrow = ' >'
    right_arrow_denied = '  '

    descriptions_margin = 1

    width_of_name_column = 0
    for name in names:
        if len(name) >= width_of_name_column:
            width_of_name_column = len(name) + 4
    left_margin = C_W // 2 - (width_of_name_column + 4) // 2

    sum_was_lesser = sum_was_greater = False
    while 1:
        draw_title_and_subheading(title, subheading + ' ({}/{} spent)'.format(sum(values), max_sum_of_values))
        _draw_line_at_the_bottom('Use UP/DOWN or 8/2 to move the cursor, LEFT/RIGHT or 4/6 to change values.')

        if sum_was_lesser or sum(values) < min_sum_of_values:
            CW.setForegroundColor(196, 32, 32)
            CW.putString('Sum of values should be greater or equal to {}    '.format(min_sum_of_values), 0, C_H-2)
            sum_was_lesser = False
        elif sum_was_greater or sum(values) > max_sum_of_values:
            CW.setForegroundColor(196, 32, 32)
            CW.putString('Sum of values should be lesser or equal to {}      '.format(max_sum_of_values), 0, C_H-2)
            sum_was_greater = False
        elif max_sum_of_values >= sum(values) >= min_sum_of_values:
            CW.setForegroundColor(32, 196, 32)
            CW.putString('You can press ENTER to confirm your choice.                   ', 0, C_H - 2)

        CW.setForegroundColor(names_color)
        for i, name in enumerate(names):
            if i == cursor_line:
                CW.setForegroundColor(0, 0, 0)
                CW.setBackgroundColor(names_color)
            else:
                CW.setForegroundColor(names_color)
                CW.setBackgroundColor(0, 0, 0)
            CW.putString('   ' +name+'    ', left_margin-3, 3+i)

            left_bracket = left_arrow if values[i] > min_permitted_value else left_arrow_denied
            right_bracket = right_arrow if values[i] < max_permitted_value and sum(values) < max_sum_of_values else right_arrow_denied
            value_to_put = '0'+str(values[i]) if values[i] < 10 else str(values[i])
            CW.putString("{}{}{}".format(left_bracket, value_to_put, right_bracket),
                         left_margin + width_of_name_column, 3+i)

            CW.setBackgroundColor(0, 0, 0)
            if descriptions is not None:
                CW.setForegroundColor(descriptions_color)
                CW.put_wrapped_text_in_rect(descriptions[cursor_line], descriptions_margin, C_H - 13, C_W-descriptions_margin, 10)
        CW.setBackgroundColor(0, 0, 0)
        CW.flushConsole()

        # KEYBOARD
        key = CW.readKey()
        if key.keychar == 'DOWN' or key.text == '2':
            cursor_line += 1
            if cursor_line >= items_in_menu:
                cursor_line = 0
        elif key.keychar == 'UP' or key.text == '8':
            cursor_line -= 1
            if cursor_line < 0:
                cursor_line = items_in_menu - 1
        elif key.keychar == 'RIGHT' or key.text == '6':
            if values[cursor_line] >= max_permitted_value or sum(values) >= max_sum_of_values:
                sum_was_greater = True
            else:
                values[cursor_line] += 1
        elif key.keychar == 'LEFT' or key.text == '4':
            if values[cursor_line] <= min_permitted_value:
                sum_was_lesser = True
            else:
                values[cursor_line] -= 1

        elif key.keychar.__contains__('ENTER'):
            if max_sum_of_values >= sum(values) >= min_sum_of_values:
                return values
        elif key.keychar == 'ESCAPE':
            # cancel selection
            return []


def keyboard_input_menu(title, subheading, min_length, max_length, default_value=''):

    left_margin = C_W // 2 - max_length // 2 - 2
    upper_margin = 4

    border_color = (160, 128, 160)
    label_color = (128, 128, 128)

    value = default_value

    draw_title_and_subheading(title, subheading, 2, True)

    # firstly, print the borders
    while True:
        for x in range(max_length + 2):
            for y in range(3):
                if (x == 0 or x == max_length+1) and (y == 0 or y == 2):
                    border_char = '+'
                elif x == 0 or x == max_length+1:
                    border_char = '|'
                elif y == 0 or y == 2:
                    border_char = '-'
                else:
                    border_char = ' '
                CW.setForegroundColor(border_color)
                CW.putChar(border_char, left_margin + x, upper_margin + y)
        CW.setForegroundColor(label_color)
        string_margin = max_length // 2 - len(value) // 2 + 1
        CW.putString(value, left_margin+string_margin, upper_margin+1)

        # print decorations
        DECOR.draw_skull(1, upper_margin, align_left=True)
        DECOR.draw_skull(60, upper_margin, align_left=False)

        CW.flushConsole()

        key = CW.readKey()
        if key.keychar =='ENTER':
            if len(value) >= min_length:
                return value
            else:
                warning_string = '{} characters minimum, please.'.format(min_length)
                CW.putString(warning_string, C_W // 2 - len(warning_string) // 2, C_H-1)
        elif key.keychar =='BACKSPACE':
            if len(value) > 0:
                value = value[:-1]
        if len(value) < max_length:
            value += key.text
