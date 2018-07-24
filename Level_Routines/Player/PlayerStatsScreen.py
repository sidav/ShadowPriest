import SidavMenu as MENU
from Routines import TdlConsoleWrapper as CW
import GLOBAL_DATA.Global_Constants as GC
from ..Controllers import LevelController as LC


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
    status_text = ''

    if player.is_hidden_in_shadow():
        x, y = player.get_position()
        shadow_amount = LC.count_vision_blocking_tiles_around_coordinates(x, y)
        if shadow_amount < 4:
            status_text += 'I feel exposed. '
        elif shadow_amount == 4:
            status_text += 'I feel like I\'m in unreliable position. '
        elif shadow_amount == 5:
            status_text += 'I feel confident. '
        elif shadow_amount >= 6:
            status_text += 'I feel concealed. '
    else:
        status_text += 'I feel assailable. '

    hp = player.get_current_hitpoints()
    max_hp = player.get_max_hitpoints()

    hp_percent = player.get_hitpoints_percentage()

    if hp_percent < 10:
        status_text += "I'm probably not going to make it. "
    elif hp_percent <= 20:
        status_text += "I'm barely clinging to life. "
    elif hp_percent <= 30:
        status_text += "I'm about to faint. "
    elif hp_percent <= 40:
        status_text += "I'm badly injured. "
    elif hp_percent <= 50:
        status_text += "The pain is bearable. "
    elif hp_percent <= 60:
        status_text += "I can keep going. "
    elif hp_percent <= 70:
        status_text += "I feel a bit wearied off. "
    elif hp_percent <= 80:
        status_text += "I feel sore. "
    elif hp_percent <= 90:
        status_text += "I'm fine. "
    elif hp_percent < 100:
        status_text += "I feel well. "
    elif hp_percent == 100:
        status_text += "I'm as healthy as ever. "

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
        status_text += 'I feel something wicked in my veins! '

    painkiller_count = player.count_status_effect('PAINKILLER')
    if painkiller_count == 1:
        status_text += 'I feel my pain somewhat faded away. '
    elif painkiller_count > 1:
        status_text += 'My feelings are uncomfortably dull. '

    CW.setForegroundColor(128, 64, 128)
    CW.put_wrapped_text_in_rect(status_text, 10, 10, GC.CONSOLE_WIDTH-20, 10)
