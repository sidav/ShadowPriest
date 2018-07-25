from Level_Routines.Controllers import LevelController as LC, ActorController_Detection as AC_D
from Level_Routines.Mechanics import TurnCosts as TC
from Routines import SidavRandom as RND
from . import ActorController as AC, ActorController_Detection as ACD
from ..Events import EventCreator as EC
from ..Creators import ActorCreator as ACREATOR
from Message_Log import MessageLog as LOG

# High-level AI here. Technical things going to ActorController.

ALERTED_STATE_DURATION = 30 # In ticks. 1 turn is 10 ticks.
DISTRACTED_STATE_DURATION = 150

# CORPSES_SEEN_UNTIL_REINFORCEMENTS = 1
# total_corpses_seen = 0

ALERT_INCREMENT_FOR_PLAYER_NOTICED = 5
ALERT_INCREMENT_FOR_CORPSE_FOUND = 85
GLOBAL_ALERT_THRESHOLD = 100

global_alert_amount = 0

def control(lvl, current_actor):
    AC.do_emergency_actions_if_needed(current_actor)
    if LC.is_time_to_act(current_actor):
        decide_state(lvl, current_actor)
        if current_actor.current_state == current_actor.states.calm:
            AC.do_roam(lvl, current_actor)
        elif current_actor.current_state == current_actor.states.alerted:
            AC.do_engage(lvl, current_actor)
        elif current_actor.current_state == current_actor.states.distracted:
            AC.do_search(lvl, current_actor)


def decide_state(lvl, actor):
    global global_alert_amount
    curr_turn = lvl.get_current_turn()
    state_turns_left = actor.get_current_state_expiration_turn() - curr_turn

    if AC_D.is_actor_seeing_an_enemy(lvl, actor):
        enemy = pick_most_important_seen_enemy(lvl, actor)
        actor.set_target_unit(enemy)

        # Let's shout for attention of others.
        e_x, e_y = enemy.get_position()
        if actor.get_current_state() == actor.states.alerted: # if he's already alerted, don't make player-perceivable event
            # TODO
            pass
        else:
            AC.do_shout_for_attention_to(actor, e_x, e_y, "HERE YOU ARE! STOP RIGHT THERE!", 10)
            increase_global_alert(ALERT_INCREMENT_FOR_PLAYER_NOTICED)

        actor.set_current_state(actor.states.alerted, curr_turn + ALERTED_STATE_DURATION)
        enemy.set_hidden_in_shadow(False)  # TODO: this is bad!

    actor_state = actor.get_current_state()
    if actor_state == actor.states.alerted:
        enemy_x, enemy_y = actor.get_target_unit().get_position()
        actor.set_target_coords(enemy_x, enemy_y)

    if state_turns_left <= 0:
        if actor_state == actor.states.alerted:
            actor.set_current_state(actor.states.distracted, curr_turn + DISTRACTED_STATE_DURATION)
        elif actor_state == actor.states.distracted:
            actor.set_current_state(actor.states.calm)

    if actor_state == actor.states.calm:
        # act if seeing a lying body
        bodies = LC.get_all_bodies_on_floor()
        for body in bodies:
            if body.is_of_type('Corpse') and not body.get_was_seen_by_ai():
                bx, by = body.get_position()
                if AC_D.is_unit_seeing_position(lvl, actor, bx, by):
                    body.set_was_seen_by_ai(True)
                    LC.add_event_to_stack(EC.shout_event(actor, bx, by, 'There is a corpse here!', 15))
                    increase_global_alert(ALERT_INCREMENT_FOR_CORPSE_FOUND)

        # investigate noises
        x, y = actor.get_position()
        events = LC.get_all_events_hearable_from(x, y)
        for event in events:
            if not event.is_for_player_only():
                ex, ey = event.get_position()
                actor.set_target_coords(ex, ey)
                if event.is_suspicious():
                    actor.set_current_state(actor.states.distracted, curr_turn + DISTRACTED_STATE_DURATION)
                    return
                else:
                    actor.set_current_state(actor.states.distracted, curr_turn + 1)  # be distracted only for one tick - just for "look at this sound" behaviour.


def increase_global_alert(amount):
    global global_alert_amount
    global_alert_amount += amount
    LOG.append_warning_message('Global alert {}, added {}'.format(global_alert_amount, amount))
    if global_alert_amount > GLOBAL_ALERT_THRESHOLD:
        global_alert_amount = 0
        call_reinforcements()
        LOG.append_warning_message('Reinforcements called.')


def call_reinforcements():
    LOG.append_message('Reinforcements have been called. ')
    LC.spawn_unit_outside_player_fov(ACREATOR.create_enforcer(0, 0))
    LC.spawn_unit_outside_player_fov(ACREATOR.create_enforcer(0, 0))


def pick_most_important_seen_enemy(lvl, actor):
    enemies_list = AC_D.get_list_of_seen_enemies(lvl, actor)
    if len(enemies_list) == 1:
        return enemies_list[0]
    # TODO: write that.
    return enemies_list[0]

