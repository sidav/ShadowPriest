from .Mechanics import MeleeAttack
from .LevelInitializer import initialize_level
from GLOBAL_DATA import Global_Constants as GC
from .Player import PlayerController as P_C, Statusbar
from .Units import ActorController as A_C
from Message_Log import MessageLog as LOG
from Routines import TdlConsoleWrapper as CW
from . import LevelView
from .LevelModel import LevelModel
from .Creators import CorpseCreator
from .EventsStack import EventsStack
from Level_Routines import EventCreator as EC

player_x = player_y = 0
last_tile = '.'
redraw_map_timeout = 10
DEFAULT_REDRAW_MAP_TIMEOUT = 10
current_level = None
events_stack = None


def initialize():
    global current_level, events_stack
    current_level = LevelModel(GC.MAP_WIDTH, GC.MAP_HEIGHT)
    current_level = initialize_level(current_level)
    events_stack = EventsStack()


def melee_attack(attacker, victim):
    MeleeAttack.do_attack(attacker, victim)
    events_stack.push_event(EC.melee_attack_event(attacker, victim, 'hits the'))


def try_open_door(x, y):
    if current_level.is_door_present(x, y):
        current_level.set_door_closed(x, y, False)
        return True
    return False


def try_close_door(x, y):
    if current_level.is_door_present(x, y):
        current_level.set_door_closed(x, y)
        return True
    return False


def is_time_to_act(unit):
    current_turn = current_level.get_current_turn()
    if unit.get_next_turn_to_act() <= current_turn:
        return True
    return False


def is_item_present(x, y):
    return current_level.is_item_present(x, y)


def try_stack_items_at_coordinates(x, y):
    items = current_level.get_items_at_coordinates(x, y)
    items_count = len(items)
    stack_successful = False
    if items_count > 1:  # then attempt to stack those items
        for i in range(items_count):
            for j in range(i, items_count):
                if items[i].is_stackable_with(items[j]):
                    items[i].change_quantity_by(items[j].get_quantity())
                    current_level.remove_item_from_floor(items[j])
                    stack_successful = True
            items = current_level.get_items_at_coordinates(x, y)
            items_count = len(items)
    return stack_successful


def get_items_at_coordinates(x, y):
    while try_stack_items_at_coordinates(x, y):
        pass
    return current_level.get_items_at_coordinates(x, y)


def get_current_turn():
    return current_level.get_current_turn()


def check_dead_units():
    units = current_level.get_all_units()
    for unit in units:
        if unit.is_dead():
            current_level.remove_unit(unit)
            corpse = CorpseCreator.create_corpse_from_unit(unit)
            current_level.add_item_on_floor_without_cordinates(corpse)
            LOG.append_message('It drops dead!')
            # TODO: drop inventory of the dead unit



def try_pick_up_item(unit, item):
    x, y = unit.get_position()
    ix, iy = item.get_position()
    if (x, y) == (ix, iy):
        unit.get_inventory().add_item(item)
        current_level.remove_item_from_floor(item)
        return True
    else:
        return False


def try_drop_item(unit, item):
    x, y = unit.get_position()
    unit.get_inventory().remove_item(item)
    current_level.add_item_on_floor_at_coordinates(item, x, y)
    return True


def control():
    global current_level, redraw_map_timeout
    player = current_level.get_player()

    while not CW.isWindowClosed():
        player_looking_range = player.get_looking_range()
        player_x, player_y = player.get_position()
        peek_x, peek_y = player.get_peeking_vector()

        all_units = current_level.get_all_units()

        current_turn = current_level.get_current_turn()
        # do we need to redraw the map?
        if redraw_map_timeout == 0 or is_time_to_act(player):
            # LevelView.draw_absolutely_everything(currentLevel)
            if player.is_peeking():
                LevelView.draw_everything_in_LOS_from_position(current_level, player_x + peek_x, player_y + peek_y, player_looking_range)
            else:
                LevelView.draw_everything_in_LOS_from_position(current_level, player_x, player_y, player_looking_range)
            LOG.print_log()
            Statusbar.print_statusbar(player, current_turn)
            CW.flushConsole()
            redraw_map_timeout = DEFAULT_REDRAW_MAP_TIMEOUT

        check_dead_units()

        events_for_player = events_stack.get_player_perceivable_events()
        for event in events_for_player:
            LOG.append_message(event.get_text())
        events_stack.cleanup_events(current_turn)

        if is_time_to_act(player):
            P_C.do_key_action(current_level)
        for unit in all_units:
            if is_time_to_act(unit):
                A_C.control(current_level, unit)
        current_level.next_turn()
        redraw_map_timeout -= 1
