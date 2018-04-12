from GLOBAL_DATA import Global_Constants as GC
from .Events import EventCreator as EC
from Level_Routines.Events.EventsStack import EventsStack as ESTCK
from Message_Log import MessageLog as LOG
from Routines import TdlConsoleWrapper as CW, SidavLOS as LOS
from . import LevelView
from .Creators import CorpseCreator
from .LevelInitializer import initialize_level
from .LevelModel import LevelModel
from .Mechanics import MeleeAttack
from .Player import PlayerController as P_C, Statusbar
from .Units import ActorController as A_C
from .Units.Unit import Unit

player_x = player_y = 0
last_tile = '.'
redraw_map_timeout = 10
DEFAULT_REDRAW_MAP_TIMEOUT = 10
current_level = None
events_stack = None
events_to_show_at_player_turn = []


def initialize():
    global current_level, events_stack
    current_level = LevelModel(GC.MAP_WIDTH, GC.MAP_HEIGHT)
    current_level = initialize_level(current_level)
    events_stack = ESTCK()


def melee_attack(attacker:Unit, victim:Unit):
    if attacker.get_inventory().get_equipped_weapon() is None:
        if MeleeAttack.try_to_attack_with_bare_hands(attacker, victim):
            event = EC.attack_with_bare_hands_event(attacker, victim)
    else:
        if victim.can_be_stabbed() and attacker.get_inventory().get_equipped_weapon().is_stabbing():
            if MeleeAttack.try_to_stab(attacker, victim):
                event = EC.stab_event(attacker, victim)
        elif MeleeAttack.try_to_attack_with_weapon(attacker, victim):
            event = EC.attack_with_melee_weapon_event(attacker, victim)
    events_stack.push_event(event)


def try_open_door(unit, x, y):
    if current_level.is_door_present(x, y):
        current_level.set_door_closed(x, y, False)
        events_stack.push_event(EC.action_event(unit, 'open', 'the door', 5))
        return True
    return False


def try_close_door(unit, x, y):
    if current_level.is_door_present(x, y):
        events_stack.push_event(EC.action_event(unit, 'close', 'the door', 5))
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
            event = EC.action_event(unit, 'drop', 'dead', 3)
            events_stack.push_event(event)
            # TODO: drop inventory of the dead unit


def try_pick_up_item(unit, item):
    x, y = unit.get_position()
    ix, iy = item.get_position()
    if (x, y) == (ix, iy):
        unit.get_inventory().add_item_to_backpack(item)
        current_level.remove_item_from_floor(item)
        return True
    else:
        return False


def try_drop_item(unit, item):
    x, y = unit.get_position()
    unit.get_inventory().remove_item_from_backpack(item)
    current_level.add_item_on_floor_at_coordinates(item, x, y)
    return True


def is_event_visible_from(event, x, y, radius = 99):
    ev_x, ev_y = event.get_position()
    if (ev_x - x) ** 2 + (ev_y - y) ** 2 <= radius ** 2:
        opacity_map = current_level.get_opacity_map()
        vis_map = LOS.getVisibilityTableFromPosition(x, y, opacity_map, radius)
        if vis_map[ev_x][ev_y]:
            return True
    return False


def is_event_hearable_from(event, x, y):
    ev_x, ev_y = event.get_position()
    event_hear_radius = event.get_hear_radius()
    if (ev_x - x) ** 2 + (ev_y - y) ** 2 <= event_hear_radius ** 2:
        return True
    return False


def check_events_for_player():
    evnts = events_stack.get_player_perceivable_events()
    for e in evnts:
        events_to_show_at_player_turn.append(e)
        e.set_already_perceived()


def show_events_for_player(player):
    global events_to_show_at_player_turn
    px, py = player.get_position()
    if player.is_peeking():
        peekx, peeky = player.get_peeking_vector()
        px += peekx
        py += peeky
    looking_range = player.get_looking_range()
    heared_event_num = 0 # for drawing the noises
    for event in events_to_show_at_player_turn:
        event.set_already_perceived()
        if is_event_visible_from(event, px, py, looking_range):
            LOG.append_message(event.get_text_when_seen())
        elif is_event_hearable_from(event, px, py):
            heared_event_num += 1
            LOG.append_message('{} at {}.'.format(event.get_text_when_heard(), str(heared_event_num)))
            event_x, event_y = event.get_position()
            CW.setForegroundColor(200, 0, 0)
            CW.putChar(str(heared_event_num), event_x, event_y)
    events_to_show_at_player_turn = []


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

            show_events_for_player(player)

            LOG.print_log()
            Statusbar.print_statusbar(player, current_turn)
            CW.flushConsole()
            redraw_map_timeout = DEFAULT_REDRAW_MAP_TIMEOUT

        check_dead_units()
        check_events_for_player()
        events_stack.cleanup_events(current_turn)

        if is_time_to_act(player):
            P_C.do_key_action(current_level)
        for unit in all_units:
            if is_time_to_act(unit):
                A_C.control(current_level, unit)
        current_level.next_turn()
        redraw_map_timeout -= 1
