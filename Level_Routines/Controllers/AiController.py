from Level_Routines.Controllers import LevelController as LC, ActorController_Detection as AC_D
from Level_Routines.Mechanics import TurnCosts as TC
from Routines import SidavRandom as RND
from . import ActorController as AC, ActorController_Detection as ACD

# High-level AI here. Technical things going to ActorController.

ALERTED_STATE_DURATION = 150

def control(lvl, current_actor):
    decide_state(lvl, current_actor)
    if current_actor.current_state == current_actor.states.calm:
        AC.do_roam(lvl, current_actor)
    else:
        current_actor.spend_turns_for_action(TC.cost_for('wait'))


def decide_state(lvl, actor):
    state_turns_left = actor.get_current_state_expiration_turn() - lvl.get_current_turn()
    player = lvl.get_player()
    px, py = player.get_position()
    if AC_D.is_unit_seeing_position(lvl, actor, px, py):
        actor.set_current_state(actor.states.alerted, lvl.get_current_turn() + ALERTED_STATE_DURATION)
    elif state_turns_left > 0 and actor.get_current_state() == actor.states.alerted:
        actor.set_current_state(actor.states.distracted)
    elif state_turns_left <= 0:
        actor.set_current_state(actor.states.calm)
    else:
        pass
        # actor.set_current_state(actor.states.calm)