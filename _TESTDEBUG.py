import Routines.TdlConsoleWrapper as CW
#from Level_Routines import LevelBuilder as LevelBld
from Overworld_Routines.Overworld import Overworld
import Overworld_Routines.OverworldView as OV

#Following file is just a testing ground for any shit possible. It should not interfere with any other logic and should cause no problems when deleted.

def makeSomeTestCrap():
    crap = Overworld(80, 21)
    OV.drawOverworldMap(crap)