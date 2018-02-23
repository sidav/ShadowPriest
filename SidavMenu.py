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
    title_xcoord = (C_W // 2) - (title_width // 2)
    CW.setBackgroundColor(0, 0, 0)
    CW.setForegroundColor(bgcolor)
    CW.putString(title, title_xcoord, 0)

def single_select_menu(title='Pick a title, dummy!', subheading='Pick subheading, dummy!', items=[]):
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
        key = CW.readKey().keychar
        if key == 'DOWN':
            cursor_line += 1
            if cursor_line >= items_in_menu:
                cursor_line = 0
        elif key == 'UP':
            cursor_line -= 1
            if cursor_line < 0:
                cursor_line = items_in_menu - 1
        elif key == 'ENTER':
            return cursor_line

    pass
