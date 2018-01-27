import Routines.TdlConsoleWrapper as CW
#from Level_Routines import LevelBuilder as LevelBld
from Overworld_Routines.OverworldModel import OverworldModel
#import Overworld_Routines.OverworldView as OV
from Overworld_Routines import OverworldController as OW_Cont
import Routines.SidavLOS as LOS

from Level_Routines import LevelController as LC

#Following file is just a testing ground for any shit possible. It should not interfere with any other logic and should cause no problems when deleted.

def makeSomeTestCrap():
    # crap = Overworld(80, 21)
    # OV.drawOverworldMap(crap)

    # OW_Cont.initialize()
    # OW_Cont.control()

    # print(LOS.is_point_in_sector(5, 8, -1, 1, 5, 5, 90))
    # print(LOS.is_point_in_sector(5, 8, -1, 1, 8, 10, 90))
    # print(LOS.is_point_in_sector(5, 8, -1, 1, 2, 12, 90))

    LC.initialize()
    LC.control()
