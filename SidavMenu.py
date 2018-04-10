from Routines import TdlConsoleWrapper as CW
from GLOBAL_DATA import Global_Constants as GC

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

def draw_title_and_subheading(title, subheading):
    CW.clearConsole()
    color = (128, 128, 128)
    _draw_titlebar(title)
    CW.setForegroundColor(color)
    CW.putString(subheading, 0, 1)


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
        CW.putString(name+':  ', 0, i+2)

    CW.setForegroundColor(values_color)
    for i, value in enumerate(values):
        CW.putString(value, width_of_name_column, i + 2)

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
