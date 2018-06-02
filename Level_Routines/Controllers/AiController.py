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
    elif current_actor.current_state == current_actor.states.alerted:
        AC.do_engage(lvl, current_actor)
    elif current_actor.current_state == current_actor.states.distracted:
        AC.do_pursue(lvl, current_actor)


def decide_state(lvl, actor):
    state_turns_left = actor.get_current_state_expiration_turn() - lvl.get_current_turn()
    if AC_D.is_actor_seeing_an_enemy(lvl, actor):
        actor.set_current_state(actor.states.alerted, lvl.get_current_turn() + ALERTED_STATE_DURATION)
        enemy = pick_most_important_enemy(lvl, actor)
        enemy_x, enemy_y = enemy.get_position()
        actor.set_target_coords(enemy_x, enemy_y)
        actor.set_target_unit(enemy)
    elif state_turns_left > 0 and actor.get_current_state() == actor.states.alerted:
        actor.set_current_state(actor.states.distracted)
    elif state_turns_left <= 0:
        actor.set_current_state(actor.states.calm)
    else:
        pass
        # actor.set_current_state(actor.states.calm)


def pick_most_important_enemy(lvl, actor):
    enemies_list = AC_D.get_list_of_seen_enemies(lvl, actor)
    if len(enemies_list) == 1:
        return enemies_list[0]
    # TODO: write that.
    return enemies_list[0]

