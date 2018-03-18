import Routines.TdlConsoleWrapper as CW
from Overworld_Routines.OverworldModel import OverworldModel
#import Overworld_Routines.OverworldView as OV
from Overworld_Routines import OverworldController as OW_Cont
import Routines.SidavLOS as LOS
from Minigames.Lockpick import Lockpick

from Level_Routines import LevelController as LC, LevelView as LV
from Level_Routines.LevelModel import LevelModel as LM
import SidavMenu as MENU

#Following file is just a testing ground for any shit possible. It should not interfere with any other logic and should cause no problems when deleted.

def makeSomeTestCrap():
    # crap = Overworld(80, 21)
    # OV.drawOverworldMap(crap)

    # OW_Cont.initialize()
    # OW_Cont.control()

    # print(LOS.is_point_in_sector(5, 8, -1, 1, 5, 5, 90))
    # print(LOS.is_point_in_sector(5, 8, -1, 1, 8, 10, 90))
    # print(LOS.is_point_in_sector(5, 8, -1, 1, 2, 12, 90))

    # while(True):
    #     level = LM(80, 20)
    #     LV.draw_whole_level_map(level)
    #     CW.flushConsole()
    #     key = CW.readKey()
    #     while key.text != 'SPACE':
    #         key = CW.readKey()

    # print(MENU.single_select_menu("AHAHA MENU LOL", "Ahaha subheading lol", ['first', 'second', 'third']))
    # print(MENU.multi_select_menu("AHAHA MULTISELECT MENU LOL", "Ahaha subheading lol", ['first', 'second', 'third']))

    a = Lockpick(3, 2)
    solved = False
    while not solved:
        CW.clearConsole()
        a.draw_puzzle(20, 5)
        CW.flushConsole()
        solved = a.do_turn()

    LC.initialize()
    LC.control()
