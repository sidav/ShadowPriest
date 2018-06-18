import SidavMenu as MENU
from Routines import TdlConsoleWrapper as CW
import GLOBAL_DATA.Global_Constants as GC


def show_player_stats(player):
    title = 'MY STATS'
    subheading = ' I am the Priest known as {}.'.format(player.get_name())
    MENU.draw_title_and_subheading(title, subheading, center_subheading=True)
    stat_names = [' Health', ' Strength', ' Nimbleness', ' Endurance', ' Advertence', ' Knowledge']
    hitpoints_line = '{}/{}'.format(player.get_current_hitpoints(), player.get_max_hitpoints())
    stat_values = [hitpoints_line] + player.get_rpg_stats().get_stats_array()
    for i in range(len(stat_names)):
        CW.putString(stat_names[i], GC.CONSOLE_WIDTH // 2 - len(stat_names[i]) - 1, i + 3)
    for i in range(len(stat_values)):
        CW.putString(str(stat_values[i]), GC.CONSOLE_WIDTH // 2 + 1, i + 3)
    make_and_print_status_text(player)
    CW.flushConsole()
    CW.readKey()
    # MENU.name_value_menu(title, subheading, stat_names, stat_values)


def make_and_print_status_text(player):
    status_text = 'I feel confident. '
    hp = player.get_current_hitpoints()
    max_hp = player.get_max_hitpoints()
    # is healing now?
    healing_count = player.count_status_effect('HEALING')
    if healing_count == 1:
        if hp == max_hp:
            status_text += 'I feel my old scars tightening. '
        else:
            status_text += 'I feel my wounds shrinking. '
    elif healing_count > 1:
        if hp == max_hp:
            status_text += 'I feel my skin crawling! '
        else:
            status_text += 'I feel a burning in my healing wounds! '

    poison_count = player.count_status_effect('POISON')
    if poison_count == 1:
        status_text += 'I feel sick. '
    elif poison_count > 1:
        status_text += 'I feel something wicked in my veins!'

    CW.setForegroundColor(128, 64, 128)
    CW.put_wrapped_text_in_rect(status_text, 10, 10, GC.CONSOLE_WIDTH-10, 10)
