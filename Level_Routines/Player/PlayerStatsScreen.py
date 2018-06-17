import SidavMenu as MENU
from Routines import TdlConsoleWrapper as CW


def show_player_stats(player):
    title = 'MY STATS'
    subheading = ' I am the Priest known as {}'.format(player.get_name())
    stat_names = [' Strength', ' Nimbleness', ' Endurance', ' Advertence', ' Knowledge']
    stat_values = player.get_rpg_stats().get_stats_array()
    MENU.name_value_menu(title, subheading, stat_names, stat_values)
