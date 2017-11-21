import Routines.TdlConsoleWrapper as CW
import Procedurals.BSPDungeonGenerator as BSP
import TitleScreen
import _TESTDEBUG as _TESTDBG_

CONSOLE_WIDTH = 80
CONSOLE_HEIGHT = 25
LOG_HEIGHT = 4
MAP_WIDTH = CONSOLE_WIDTH
MAP_HEIGHT = CONSOLE_HEIGHT - LOG_HEIGHT


def main():
    CW.initConsole(CONSOLE_WIDTH, CONSOLE_HEIGHT, "ShadowPriest")
    #CW.putString("Shadow Priest window operational!", 0, 0)
    #CW.drawCharArray(BSP.generateMap())
    TitleScreen.drawTitle()

    _TESTDBG_.makeSomeTestCrap()# <--- SHOULD BE SAFELY DELETED!
    print("Oooh Long Johnson")
    while not CW.isWindowClosed():
        CW.flushConsole()
















if __name__ == '__main__':
    main()