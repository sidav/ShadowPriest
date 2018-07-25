from Level_Routines import LevelView
from Level_Routines.Controllers import LevelController as LC, UnitController as UC, PlayerController_Inventory as PC_I
from Level_Routines.Mechanics import TurnCosts as TC
from Message_Log import MessageLog as LOG
from Routines import TdlConsoleWrapper as CW, SidavRandom as RND
from GLOBAL_DATA import Level_Tile_Data as LTD, Global_Constants as GC
import SidavMenu as MENU
from .. import Debugging as DBG
from ..Player import PlayerStatsScreen as STATSCREEN, HelpScreen as HELPSCREEN
from ..Player import DeathScreen

# player_has_spent_time = False


def do_key_action(lvl):
    # global player_has_spent_time
    # player_has_spent_time = False
    player = lvl.get_player()

    if player.is_dead():
        DeathScreen.show_death_screen(player)


    if player.is_peeking():
        continue_peeking(player)
        return

    if player.is_lockpicking():
        continue_lockpicking(player)
        return

    while not player_has_spent_time(player):
        LOG.print_log()
        CW.flushConsole()
        keyPressed = CW.readKey()

        DBG.do_debug_key(keyPressed) # <-- Delete it somewhen!

        key_text = keyPressed.text

        if keyPressed.text != '':
            if 1040 <= ord(list(keyPressed.text)[0]) <= 1103:
                LOG.append_message('I feel like I should change my keyboard layout to EN.')

        if not do_move_keys_action(lvl, player, key_text):
            if keyPressed.text == '5' or keyPressed.text == ' ':
                wait_or_hide(player)
            if key_text == '-':
                LevelView.SINGLE_ARROW_MODE ^= True # "some_bool ^= True" is equivalent to "some_bool = not some_bool"
                LOG.append_replaceable_message("Single arrow mode set to {0}".format(bool(LevelView.SINGLE_ARROW_MODE)))
            if keyPressed.key == 'F1': # show help
                HELPSCREEN.show_help()
                LC.force_redraw_screen()
            if keyPressed.text == 'c': # close door
                try_close_door(lvl, player)
            if keyPressed.text == 'p': # peek
                do_peeking(lvl, player)
            if keyPressed.text == 's': # strangle
                do_ko_attack(lvl, player)
            if keyPressed.text == 'g': # grab
                PC_I.do_grabbing(player)
                LC.force_redraw_screen()
            if keyPressed.text == 'G': # lay out items from body
                do_body_searching(player)
            if keyPressed.text == 'd': # drop
                PC_I.do_dropping(player)
                LC.force_redraw_screen()
            if keyPressed.text == 'w': # wield
                PC_I.do_wielding(player)
                LC.force_redraw_screen()
            if keyPressed.text == 'R': # quiver / ready ammo
                PC_I.do_quivering(player)
                LC.force_redraw_screen()
            if keyPressed.text == 'q': # Quaff a potion
                PC_I.do_quaffing(player)
                LC.force_redraw_screen()
            if keyPressed.text == 'f': # fire ranged weapon in hands
                do_firing(lvl, player)
                LC.force_redraw_screen()
            if keyPressed.text == 'r': # reload weapon
                do_reloading(player)
            if keyPressed.text == 'N': # make a noise
                do_noising(player)
            if keyPressed.text == 'P': # pick a lock
                do_lockpicking(lvl, player)
            if keyPressed.text == '@': # show player stats
                STATSCREEN.show_player_stats(player)
                LC.force_redraw_screen(True)
            # if keyPressed.text == 'U': # unwield
            #     PC_I.do_unwielding(player)
            if keyPressed.text == 'i': # list equipped items
                PC_I.show_equipped_items(player)
                LC.force_redraw_screen()
            if keyPressed.text == '>': # descend the stairs
                do_descend(player)


def player_has_spent_time(player):
    return player.get_next_turn_to_act() > LC.get_current_turn()


# def spend_time(player, action_name=''): # deprecated
#     # global player_has_spent_time
#     if action_name != '':
#         player.spend_turns_for_action(TC.cost_for(action_name))
#     # player_has_spent_time = True


def do_descend(player):
    x, y = player.get_position()
    from ..Player import EndgameScreen
    if LC.are_downstairs_present(x, y):
        EndgameScreen.show_endgame_screen(False)
    elif GC.DEBUG_ENABLED:
        EndgameScreen.show_endgame_screen(True)
    else:
        LOG.append_message('I see no downstairs there.')


def wait_or_hide(player):
    if not player.is_hidden_in_shadow():
        if UC.try_hide_in_shadow(player):
            notification_variant = RND.rand(3)
            if notification_variant == 0:
                LOG.append_message('I fall into shadows.')
            elif notification_variant == 1:
                LOG.append_message('I nestle in the dark.')
            elif notification_variant == 2:
                LOG.append_message('I vanish in darkness.')
            return
    player.spend_turns_for_action(TC.cost_for('wait'))
    LOG.append_message('I wait for a sec. ')
    return


def do_move_keys_action(lvl, player, key):
    vector_x, vector_y = key_to_direction(key)
    if vector_x == vector_y == 0:
        return False
    px, py = player.get_position()
    target_x, target_y = px + vector_x, py + vector_y
    if lvl.is_door_present(target_x, target_y):
        lock_level = LC.get_tile_lock_level(target_x, target_y)
        if lock_level > 0 and not lvl.is_tile_passable(target_x, target_y):
            if player.get_inventory().has_key_of_lock_level(lock_level):
                LOG.append_message('I unlock the door with my key.')
            else:
                LOG.append_message("I need a {} key to open that door.".format(LTD.door_lock_level_names[lock_level]))
    time_spent = UC.try_make_directional_action(lvl, player, vector_x, vector_y)
    if time_spent:
        if player.is_hidden_in_shadow():                                               ##
            if UC.try_to_be_not_exposed_from_shadow(player):                            #
                notification_variant = RND.rand(5)                                      #
                if notification_variant == 0:                                           #
                    LOG.append_message('I stick to shadows.')                           #
                elif notification_variant == 1:                                         #
                    LOG.append_message('Darkness conceals my movement.')                #
        #                                                                               # FUCKING
            else:                                                                       # BAD
                player.set_hidden_in_shadow(False)                                      # PRACTICE
                notification_variant = RND.rand(2)                                      # (the logic needs to be moved
                if notification_variant == 0:                                           # to UnitController!)
                    LOG.append_message('I accidentally expose myself to a light.')      #
                elif notification_variant == 1:                                         #
                    LOG.append_message('Shadow betrays me.')                           ##

    if (px, py) != player.get_position(): # i.e. player has moved this turn 
        notify_for_anything_on_floor(lvl, player)
    return True


def try_close_door(lvl, player):
    px, py = player.get_position()
    to_x, to_y = ask_for_direction('Where to close a door?')
    if lvl.is_door_present(px+to_x, py+to_y):
        if LC.try_close_door(player, px+to_x, py+to_y):
            pass
        else:
            LOG.append_message("I can't close the door! ")
            player.spend_turns_for_action(TC.cost_for('close door'))
    else:
        LOG.append_message('There is no door here!')


def do_peeking(lvl, player):
    px, py = player.get_position()
    peek_x, peek_y = ask_for_direction('Peek in which direction?')
    if not (lvl.is_door_present(px + peek_x, py + peek_y) or lvl.is_tile_passable(px + peek_x, py + peek_y)):
        LOG.append_message("I can't peek there! ")
        return
    player.set_peeking(True)
    player.set_peeking_vector(peek_x, peek_y)
    LOG.append_message('I carefully peek there... ')
    LOG.append_replaceable_message('I can pass turns with space or 5 to continue peeking.')
    player.spend_turns_for_action(TC.cost_for('peek'))


def continue_peeking(player):
    LOG.append_replaceable_message('I continue peeking... ')
    keyPressed = CW.readKey()
    if keyPressed.text != '5' and keyPressed.text != ' ':
        player.set_peeking(False)
        LOG.append_message('I recoil and look around. ')
    else:
        player.spend_turns_for_action(TC.cost_for('peek'))


def do_lockpicking(lvl, player):
    px, py = player.get_position()
    if player.get_inventory().is_carrying_body_on_shoulder():
        LOG.append_message("I can't pick a lock with that burden on my shoulder.")
        return 
    pick_x, pick_y = ask_for_direction('Pick which lock?')
    x, y = px + pick_x, py + pick_y
    if not lvl.is_door_present(x, y):
        LOG.append_message("I see no locks there...")
        return
    if LC.get_tile_lock_level(x, y) == 0 or lvl.is_tile_passable(x, y):
        LOG.append_message("No need to pick a lock there.")
        return

    player.set_lockpicking(True)
    player.set_peeking_vector(pick_x, pick_y)

    LOG.append_message('I prepare my lockpicks... ')
    LOG.append_replaceable_message('Use ESC to cancel.')
    minigame = LC.get_lockpicking_minigame_for_door(x, y)
    minigame.draw_puzzle()
    keyPressed = CW.readKey()
    if keyPressed.keychar == 'ESCAPE':
        player.set_lockpicking(False)
        LOG.append_message('I recoil and look around. ')
        player.spend_turns_for_action(TC.cost_for('lockpicking step'))
        return
    minigame.do_turn(keyPressed)
    player.spend_turns_for_action(TC.cost_for('lockpicking step'))


def continue_lockpicking(player):
    px, py = player.get_position()
    pick_x, pick_y = player.get_peeking_vector()
    LOG.append_message('I continue picking the lock... ')
    minigame = LC.get_lockpicking_minigame_for_door(px + pick_x, py + pick_y)
    minigame.draw_puzzle()

    keyPressed = CW.readKey()
    if keyPressed.keychar == 'ESCAPE':
        player.set_lockpicking(False)
        LOG.append_message('I recoil and look around. ')
        player.spend_turns_for_action(TC.cost_for('lockpicking step'))
        return
    result = minigame.do_turn(keyPressed)
    if result:
        LOG.append_message('I successfully open the lock!')
        LC.set_door_closed(px + pick_x, py + pick_y, False)
        player.set_lockpicking(False)
    player.spend_turns_for_action(TC.cost_for('lockpicking step'))


def notify_for_anything_on_floor(lvl, player):
    px, py = player.get_position()
    if lvl.is_stairs_present(px, py):
        LOG.append_message('I am standing at the {}.'.format(lvl.get_stairs_name(px, py)))
    if LC.is_item_present(px, py):
        item_message = 'I see here: '
        items_here = LC.get_items_at_coordinates(px, py)
        item_message += items_here[0].get_name()
        if len(items_here) > 1:
            item_message += ' and {} more items'.format(len(items_here)-1)
        item_message += '.'
        LOG.append_message(item_message)
        # LC.force_redraw_screen()


def do_ko_attack(lvl, player):
    px, py = player.get_position()
    grab_x, grab_y = ask_for_direction('Grab whom?')
    if grab_x == 0 and grab_y == 0:
        LOG.append_message("I don't find it funny.")
        return 
    target_x = px + grab_x
    target_y = py + grab_y
    if lvl.is_unit_present(target_x, target_y):
        target_unit = lvl.get_unit_at(target_x, target_y)
        LC.knockout_attack(player, target_unit)
    else:
        LOG.append_message('There is nobody here!')


def do_body_searching(player):
    x, y = player.get_position()
    if LC.is_body_present_at(x, y):
        if LC.is_any_body_at_unit_coords_not_searched(player):
            if LC.try_lay_out_items_from_body(player):
                LOG.append_message("I've laid out items from the body on floor.")
            else:
                LOG.append_message("I've searched the body, but found nothing.")
        else:
            LOG.append_message("I've already searched everything here.")
    else:
        LOG.append_message('There are no bodies here!')


def do_noising(player):
    noise_amount = RND.rand(3)+3
    LOG.append_warning_message('noise radius is {}'.format(noise_amount))
    UC.make_noise(player, 'clap', 'my hands', noise_amount, 10)
    

def do_reloading(player):
    inv = player.get_inventory()
    weapon = inv.get_equipped_weapon()
    if weapon is None:
        LOG.append_message('I have nothing to reload!')
        return
    if not weapon.is_of_type('RangedWeapon'):
        LOG.append_message("The {} can't be reloaded!".format(weapon.get_name()))
        return
    ammo_in_ready = inv.get_equipped_ammo()
    ammo_in_weapon = weapon.get_loaded_ammunition()
    rem_ammo = weapon.get_remaining_ammunition_count()
    max_ammo = weapon.get_max_ammunition()
    if rem_ammo == max_ammo and ammo_in_ready.is_stackable_with(ammo_in_weapon):
        LOG.append_message("My {} is already loaded.".format(weapon.get_name(False)))
        return
    if ammo_in_ready is None:
        LOG.append_message("I don't have ammo for my {} in ready!".format(weapon.get_name(False)))
        return
    if LC.try_reload_unit_weapon(player):
        return
        # spend_time(player)
    else:
        LOG.append_error_message("can't reload {} for unknown reason".format(weapon.get_name()))


def do_firing(lvl, player):
    px, py = player.get_position()
    inv = player.get_inventory()
    weapon = inv.get_equipped_weapon()
    # Firstly, check if we can fire at all.
    if weapon is None:
        LOG.append_message('I have nothing to fire with!')
        return
    if not weapon.is_of_type('RangedWeapon'):
        LOG.append_message("I can't shoot with the {}!".format(weapon.get_name()))
        return
    # if weapon.get_loaded_ammunition() is None or weapon.get_loaded_ammunition().get_quantity() == 0:
    #     LOG.append_message("I am out of my ammo!".format(weapon.get_name()))
    #     return

    # Secondly, pick the target.
    tx, ty = ask_for_target(player)
    # Aaaaand... shoot or not. 
    if tx == px and ty == py:
        LOG.append_message("Wanna end it all huh?")
        return
    elif tx == ty == -1:
        LOG.append_message("Okely-dokely.")
        return
    else:
        LC.ranged_attack(player, tx, ty)
        # spend_time(player)


################ Technical code below ################################


def ask_for_target(player, log_text='Pick a target...'):
    LOG.append_message(log_text)
    tx, ty = player.get_position()
    while True:
        LC.force_redraw_screen(flush=False)
        if LC.is_unit_present_at(tx, ty):
            CW.setForegroundColor(196, 0, 0)
        else:
            CW.setForegroundColor(196, 196, 0)
        CW.putChar('X', tx, ty)
        CW.flushConsole()
        key = CW.readKey()
        if key.keychar == 'ESCAPE':
            return -1, -1
        elif key.keychar == 'ENTER' or key.keychar == 'SPACE' or key.text == 'f':
            return tx, ty
        direction = key_to_direction(key.text)
        tx += direction[0]
        ty += direction[1]


def ask_for_direction(log_text='Pick a direction...'):
    LOG.append_replaceable_message(log_text)
    keyPressed = CW.readKey()
    return key_to_direction(keyPressed.text)


def key_to_direction(key):
    vector_x = vector_y = 0
    if key == 'h' or key == '4':
        vector_x = -1
    elif key == 'j' or key == '2':
        vector_y = 1
    elif key == 'k' or key == '8':
        vector_y = -1
    elif key == 'l' or key == '6':
        vector_x = 1
    elif key == 'y' or key == '7':
        vector_x = -1
        vector_y = -1
    elif key == 'u' or key == '9':
        vector_x = 1
        vector_y = -1
    elif key == 'b' or key == '1':
        vector_x = -1
        vector_y = 1
    elif key == 'n' or key == '3':
        vector_x = 1
        vector_y = 1
    return vector_x, vector_y
