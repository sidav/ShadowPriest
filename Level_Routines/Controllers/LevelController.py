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
from . import PlayerController as P_C, AiController as AI, UnitController as U_C, StatusEffectsController as SEC
from Level_Routines.Units.Unit import Unit

player_x = player_y = 0
last_tile = '.'
redraw_map_timeout = 10
DEFAULT_REDRAW_MAP_TIMEOUT = 10
current_level = None
events_stack = None
events_to_show_at_player_turn = []


def initialize(player):
    global current_level, events_stack
    current_level = LevelModel(GC.MAP_WIDTH, GC.MAP_HEIGHT)
    current_level = initialize_level(current_level, player)
    U_C.set_current_level(current_level)
    events_stack = ESTCK()


def add_event_to_stack(event):
    events_stack.push_event(event)


def knockout_attack(attacker:Unit, victim:Unit):  # TODO: chances and shit
    if Knockout.try_to_knockout(attacker, victim):
        KO_time = Knockout.calculate_knockout_time(attacker, victim)
        drop_equipped_items(victim)
        current_level.remove_unit(victim)
        body = BodyCreator.create_unconscious_body_from_unit(victim, get_current_turn() + KO_time)
        current_level.add_item_on_floor_without_cordinates(body)
        event = EC.knockout_attack_event(attacker, victim)
    else:
        event = EC.action_event(attacker, 'failed to strangle', victim.get_name(), 2)
    events_stack.push_event(event)


def ranged_attack(attacker:Unit, target_x, target_y):
    attacker_weapon = attacker.get_inventory().get_equipped_weapon()

    if attacker_weapon.get_loaded_ammunition() is None or attacker_weapon.get_loaded_ammunition().get_quantity() == 0:
        event = EC.empty_ammo_shooting_event(attacker, '*Click!*')
        attacker.spend_turns_for_action(TC.cost_for('firing'))
        events_stack.push_event(event)
        return

    if is_unit_present_at(target_x, target_y):
        victim = current_level.get_unit_at(target_x, target_y)

        if RangedAttack.try_to_shoot(attacker, victim):
            event = EC.ranged_attack_event(attacker, victim)
        else:
            event = EC.missed_ranged_attack_event(attacker, victim)
    else:
        # TODO: "shooting at things" code here
        attacker_weapon.get_loaded_ammunition().change_quantity_by(-1)
        attacker.spend_turns_for_action(TC.cost_for('firing'))
        return
    attacker.spend_turns_for_action(TC.cost_for('firing'))
    events_stack.push_event(event)


def get_tile_lock_level(x, y):
    return current_level.get_tile_lock_level(x, y)


def get_lockpicking_minigame_for_door(x, y):
    return current_level.get_lockpicking_minigame_for_door(x, y)


def set_door_closed(x, y, b):
    current_level.set_door_closed(x, y, b)


def try_open_door(unit, x, y):
    if current_level.is_door_present(x, y):
        lock_level = current_level.get_tile_lock_level(x, y)
        if lock_level == 0 or unit.get_inventory().has_key_of_lock_level(lock_level):
            current_level.set_door_closed(x, y, False)
            events_stack.push_event(EC.action_event(unit, 'open', 'the door', 5))
            return True
        else:
            # LOG.append_warning_message('Attempt to open a door with no appropriate key!')
            pass
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
        unit.set_next_turn_to_act(current_turn)
        return True
    return False


def is_item_present(x, y):
    return current_level.is_item_present(x, y)


def is_body_present_at(x, y):
    items = current_level.get_items_at_coordinates(x, y)
    for item in items:
        if item.is_body():
            return True
    return False


def is_unit_present_at(x, y):
    return current_level.is_unit_present(x, y)


def get_unit_at(x, y):
    return current_level.get_unit_at(x, y)


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


def get_bodies_at_coordinates(x, y):
    return current_level.get_bodies_at_coordinates(x, y)


def get_current_turn():
    return current_level.get_current_turn()


def drop_equipped_items(unit):
    x, y = unit.get_position()
    items = [
        unit.get_inventory().remove_equipped_weapon(),
        unit.get_inventory().remove_equipped_ammo()
    ]
    for item in items:
        if item is not None:
            current_level.add_item_on_floor_at_coordinates(item, x, y)


def check_dead_units():
    units = current_level.get_all_units()
    for unit in units:
        if unit.is_dead():
            drop_equipped_items(unit)
            current_level.remove_unit(unit)
            corpse = BodyCreator.create_corpse_from_unit(unit)
            current_level.add_item_on_floor_without_cordinates(corpse)
            event = EC.action_event(unit, 'drop', 'dead', 3)
            events_stack.push_event(event)
            # TODO: drop inventory of the dead unit


def check_unconscious_bodies():
    items = current_level.get_all_items_on_floor()
    for item in items:
        if item.__class__.__name__ == 'UnconsciousBody':
            x, y = item.get_position()
            if item.get_time_for_wake_up() <= get_current_turn() and not current_level.is_unit_present(x, y):
                current_level.remove_item_from_floor(item)
                unit = item.get_original_unit()
                unit.set_coordinates(x, y)
                unit.set_next_turn_to_act(get_current_turn() + 10)
                current_level.spawn_unit(unit)
                event = EC.action_event(unit, 'wake', 'up', 3)
                events_stack.push_event(event)


def try_pick_up_item(unit, item):
    x, y = unit.get_position()
    ix, iy = item.get_position()
    if (x, y) == (ix, iy):
        if item.is_body():
            if unit.get_inventory().get_body_on_shoulder() is None:
                unit.get_inventory().pick_body_on_shoulder(item)
            else:
                return False
        else:
            unit.get_inventory().add_item_to_backpack(item)

        current_level.remove_item_from_floor(item)
        unit.get_inventory().try_stack_items_in_backpack()
        return True
    else:
        return False


def try_drop_item(unit, item):
    x, y = unit.get_position()
    if item.is_body():
        unit.get_inventory().remove_body_from_shoulder()
    else:
        unit.get_inventory().remove_item_from_backpack(item)
    current_level.add_item_on_floor_at_coordinates(item, x, y)
    return True


def try_lay_out_items_from_body(acting:Unit):
    x, y = acting.get_position()
    bodies = get_bodies_at_coordinates(x, y)
    if len(bodies) == 0:
        return False
    else:
        for body in bodies:
            if not body.get_inventory().is_backpack_empty():
                drop_all_items_from_body(body)
                return True
    return False


def drop_all_items_from_body(body):
    x, y = body.get_position()
    inv = body.get_inventory()
    backpack = inv.get_backpack()
    for item in backpack:
        current_level.add_item_on_floor_at_coordinates(item, x, y)
    body.empty_backpack()
    body.set_searched()


def try_reload_unit_weapon(unit):
    inv = unit.get_inventory()
    weapon = inv.get_equipped_weapon()
    ammo_in_ready = inv.get_equipped_ammo()

    if weapon is not None and weapon.is_of_type('RangedWeapon') and ammo_in_ready is not None:
        ammo_in_weapon = weapon.get_loaded_ammunition()
        # if the weapon is already loaded with same ammo that is quivered...
        if ammo_in_weapon is not None and weapon.can_be_refilled_with(ammo_in_ready):
            # LOG.append_warning_message('path 1')
            remaining_ammo_to_full = weapon.get_max_ammunition() - ammo_in_weapon.get_quantity()
            if ammo_in_ready.get_quantity() > remaining_ammo_to_full:
                # LOG.append_warning_message('Quivered is enough')
                ammo_in_weapon.change_quantity_by(remaining_ammo_to_full)
                ammo_in_ready.change_quantity_by(-remaining_ammo_to_full)
            else:
                # LOG.append_warning_message('Spending all quiver')
                ammo_in_weapon.change_quantity_by(ammo_in_ready.get_quantity())
                ammo_in_ready.set_quantity(0)
            events_stack.push_event(EC.action_event(unit, 'reload', 'the {}'.format(weapon.get_name(False)), 3))
            unit.spend_turns_for_action(TC.cost_for('Reloading', unit))
            return True
        # else: weapon is not loaded or loaded ammo type is mismatched.
        elif weapon.can_be_loaded_with(ammo_in_ready):
            # LOG.append_warning_message('path 2')
            inv.add_item_to_backpack(ammo_in_weapon)
            remaining_ammo_to_full = weapon.get_max_ammunition()
            if ammo_in_ready.get_quantity() > remaining_ammo_to_full:
                # LOG.append_warning_message('Quivered is enough')
                ammo_to_load = ammo_in_ready.pick_amount_from_stack(remaining_ammo_to_full)
                weapon.load_ammunition(ammo_to_load)
            else:
                # LOG.append_warning_message('Spending all quiver')
                weapon.load_ammunition(ammo_in_ready)
                inv.empty_equipped_ammo()
            events_stack.push_event(EC.action_event(unit, 'reload', 'the {}'.format(weapon.get_name(False)), 3))
            unit.spend_turns_for_action(TC.cost_for('Changing loaded ammo', unit))
            return True
    return False


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


def get_all_events_hearable_from(x, y):
    events = events_stack.get_active_events()
    hearable = []
    for e in events:
        if is_event_hearable_from(e, x, y):
            hearable.append(e)
    return hearable


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


def get_passability_map_for(unit):
    map = [[False] * GC.MAP_HEIGHT for _ in range(GC.MAP_WIDTH)]
    for x in range(GC.MAP_WIDTH):
        for y in range(GC.MAP_HEIGHT):
            if current_level.is_tile_passable(x, y):
                map[x][y] = True
            elif current_level.is_door_present(x, y):
                lock_level = current_level.get_tile_lock_level(x, y)
                if lock_level == 0 or unit.get_inventory().has_key_of_lock_level(lock_level):
                    map[x][y] = True
    return map


def force_redraw_screen(flush=True):  # deprecated to use outside of control() or UI-only modules
    global redraw_map_timeout
    player = current_level.get_player()
    current_turn = current_level.get_current_turn()
    player_looking_range = player.get_looking_range()
    player_x, player_y = player.get_position()
    peek_x, peek_y = player.get_peeking_vector()
    if player.is_peeking():
        LevelView.draw_everything_in_LOS_from_position(current_level, player_x + peek_x, player_y + peek_y,
                                                       player_looking_range)
    else:
        LevelView.draw_everything_in_LOS_from_position(current_level, player_x, player_y, player_looking_range)
    show_events_for_player(player)
    LOG.print_log()
    Statusbar.print_statusbar(player, current_turn)
    if flush:
        CW.flushConsole()
    redraw_map_timeout = DEFAULT_REDRAW_MAP_TIMEOUT


def control():
    global current_level, redraw_map_timeout
    player = current_level.get_player()

    while not CW.isWindowClosed():
        # player_looking_range = player.get_looking_range()
        # player_x, player_y = player.get_position()
        # peek_x, peek_y = player.get_peeking_vector()

        all_units = current_level.get_all_units()

        current_turn = current_level.get_current_turn()
        # do we need to redraw the map?
        if redraw_map_timeout == 0 or is_time_to_act(player):
            check_events_for_player() # DOUBLED BELOW! Not a mistake!
            force_redraw_screen()


            # # LevelView.draw_absolutely_everything(currentLevel)
            # if player.is_peeking():
            #     LevelView.draw_everything_in_LOS_from_position(current_level, player_x + peek_x, player_y + peek_y, player_looking_range)
            # else:
            #     LevelView.draw_everything_in_LOS_from_position(current_level, player_x, player_y, player_looking_range)
            #
            # show_events_for_player(player)
            #
            # LOG.print_log()
            # Statusbar.print_statusbar(player, current_turn)
            # CW.flushConsole()
            # redraw_map_timeout = DEFAULT_REDRAW_MAP_TIMEOUT

        check_dead_units()
        check_unconscious_bodies()
        check_events_for_player() # DOUBLED ABOVE! NOT A MISTAKE!
        events_stack.cleanup_events(current_turn)

        if current_turn % 10 == 0:
            SEC.apply_status_effects_to_a_unit(player)
        if is_time_to_act(player):
            P_C.do_key_action(current_level)

        for unit in all_units:
            if current_turn % 10 == 0:
                SEC.apply_status_effects_to_a_unit(unit)
            if is_time_to_act(unit):
                AI.control(current_level, unit)
        current_level.next_turn()
        redraw_map_timeout -= 1
