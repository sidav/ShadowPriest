from GLOBAL_DATA import Global_Constants as GC
from Level_Routines.Mechanics import TurnCosts as TC
from Level_Routines.Events import EventCreator as EC
from Level_Routines.Events.EventsStack import EventsStack as ESTCK
from Message_Log import MessageLog as LOG
from Routines import TdlConsoleWrapper as CW, SidavLOS as LOS
from Level_Routines import LevelView
from Level_Routines.Creators import BodyCreator
from Level_Routines.LevelInitializer import initialize_level
from Level_Routines.LevelModel import LevelModel
from Level_Routines.Mechanics import MeleeAttack, Knockout, RangedAttack
from Level_Routines.Player import Statusbar
from . import LevelController as LC, PlayerController as P_C, ActorController as A_C
from Level_Routines.Units.Unit import Unit

levelmodel = None


# All unit actions (when they're applicable for both player and actors) are here.


def set_current_level(level):
    global levelmodel
    levelmodel = level


def try_move_forward(unit):
    posx, posy = unit.get_position()
    lookx, looky = unit.get_look_direction()
    if levelmodel.is_tile_passable(posx + lookx, posy + looky):
        unit.move_forward()
        unit.spend_turns_for_action(TC.cost_for('move'))
        return True
    return False


def try_move_by_vector(unit, x, y):
    posx, posy = unit.get_position()
    if levelmodel.is_tile_passable(posx + x, posy + y):
        unit.move_by_vector(x, y)
        unit.spend_turns_for_action(TC.cost_for('move'))
        return True
    return False
