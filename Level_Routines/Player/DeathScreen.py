from Routines import TdlConsoleWrapper as CW
from GLOBAL_DATA import Global_Constants as GC

_death_text = [
"_  _  _____  __ __ // _____ _____    _____ _____  ___  _____",
"\\\\// ((   )) || ||    ||_// ||==     ||  ) ||==  ||=|| ||  )",
" //   \\\\_//  \\\\_//    || \\\\ ||___  _ ||_// ||___ || || ||_//"

]


def _determine_x_position(arr):
    ww = GC.CONSOLE_WIDTH
    if isinstance(arr, list):
        picw = len(arr[0])
        return int((ww - picw) * 0.5)
    elif isinstance(arr, str):
        picw = len(arr)
        return int((ww - picw)*0.47)


def _determine_y_position(arr):
    wh = GC.CONSOLE_HEIGHT
    pich = len(arr)
    return int((wh-pich)/3)


def show_death_screen(player):
    CW.setForegroundColor(196, 0, 0)
    x = _determine_x_position(_death_text)
    y = _determine_y_position(_death_text)
    CW.drawCharArrayAtPosition(_death_text, x, y, True)
    CW.flushConsole()
    CW.readKey()
