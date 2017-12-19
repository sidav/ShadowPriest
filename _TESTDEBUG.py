import Routines.TdlConsoleWrapper as CW
#from Level_Routines import LevelBuilder as LevelBld
from Overworld_Routines.OverworldModel import OverworldModel
#import Overworld_Routines.OverworldView as OV
from Overworld_Routines import OverworldController as OW_Cont

#Following file is just a testing ground for any shit possible. It should not interfere with any other logic and should cause no problems when deleted.

def makeSomeTestCrap():
    # crap = Overworld(80, 21)
    # OV.drawOverworldMap(crap)
    OW_Cont.initialize()
    OW_Cont.control()