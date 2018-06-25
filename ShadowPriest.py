from GLOBAL_DATA import Global_Constants as GC
import Routines.TdlConsoleWrapper as CW
import Procedurals.BSPDungeonGenerator as BSP
import TitleScreen
import _TESTDEBUG as _TESTDBG_


def main():
    CW.initConsole(GC.CONSOLE_WIDTH, GC.CONSOLE_HEIGHT, "ShadowPriest")
    #CW.putString("Shadow Priest window operational!", 0, 0)
    #CW.drawCharArray(BSP.generateMap())

    _TESTDBG_.makeSomeTestCrap()# <--- SHOULD BE SAFELY DELETED!

    TitleScreen.drawTitle()

    # DELETE THE FOLLOWING
    from Level_Routines import main
    main.init()
    main.start_main_loop()

    while not CW.isWindowClosed():
        CW.flushConsole()













if __name__ == '__main__':
    main()