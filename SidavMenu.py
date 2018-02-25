from Routines import TdlConsoleWrapper as CW
from GLOBAL_DATA import Global_Constants as GC

C_W, C_H = GC.CONSOLE_WIDTH, GC.CONSOLE_HEIGHT
# cursor_line = 0

def draw_titlebar(title, fgcolor=(128, 128, 128), bgcolor=(128, 0, 0)):
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

def single_select_menu(title='Single Select. Pick a title, dummy!', subheading='Pick subheading, dummy!', items=[]):
    cursor_line = 0
    color = (128, 128, 128)
    items_in_menu = len(items)

    draw_titlebar(title)

    CW.setForegroundColor(color)
    CW.putString(subheading, 0, 1)
    while 1:
        for i, item in enumerate(items):
            if (i == cursor_line):
                CW.setForegroundColor(0, 0, 0)
                CW.setBackgroundColor(color)
            else:
                CW.setForegroundColor(color)
                CW.setBackgroundColor(0, 0, 0)
            CW.putString(' '+item+' ', 0, 2+i)
        CW.flushConsole()
        key = CW.readKey()
        if key.keychar == 'DOWN':
            cursor_line += 1
            if cursor_line >= items_in_menu:
                cursor_line = 0
        elif key.keychar == 'UP':
            cursor_line -= 1
            if cursor_line < 0:
                cursor_line = items_in_menu - 1
        elif key.keychar == 'ENTER' or key.text == ' ':
            return cursor_line

def multi_select_menu(title='Multi Select. Pick a title, dummy!', subheading='Pick subheading, dummy!', items=[]):
    # returns the list of indexes of selected values.
    cursor_line = 0
    color = (128, 128, 128)
    items_in_menu = len(items)
    selected_items = [False for _ in range(items_in_menu)]

    draw_titlebar(title)

    CW.setForegroundColor(color)
    CW.putString(subheading, 0, 1)
    while 1:
        for i, item in enumerate(items):
            if (i == cursor_line):
                CW.setForegroundColor(0, 0, 0)
                CW.setBackgroundColor(color)
            else:
                CW.setForegroundColor(color)
                CW.setBackgroundColor(0, 0, 0)
            if selected_items[i]:
                CW.putString(' + ' + item + ' ', 0, 2 + i)
            else:
                CW.putString(' ' + item + '   ', 0, 2+i)
        CW.flushConsole()
        key = CW.readKey()
        if key.keychar == 'DOWN':
            cursor_line += 1
            if cursor_line >= items_in_menu:
                cursor_line = 0
        elif key.keychar == 'UP':
            cursor_line -= 1
            if cursor_line < 0:
                cursor_line = items_in_menu - 1
        elif key.text == ' ':
            selected_items[cursor_line] ^= 1
        elif key.keychar == 'ENTER':
            # form a list of indeces
            result = []
            for i, bool in enumerate(selected_items):
                if bool:
                    result.append(i)
            return result
