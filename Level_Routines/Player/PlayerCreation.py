import SidavMenu as MENU
from .Player import Player


def create_player():

    player_name = MENU.keyboard_input_menu('PRIEST IS INITIATING', 'What is your name, Priest?', 3, 25, 'The Imperceptible')

    val_names = ['Strength', 'Nimbleness', 'Endurance', 'Advertence', 'Knowledge']
    descriptions = [
        'The Strength, as in physical might, is one of the primary disciplines for the Priests. The amount of effort put '
        'into Strength training indicates how strong the said priest is, how powerful his melee attacks are, how much he '
        'can carry and what kind of weapons he could use. The supposed masters of this discipline can "kill someone with '
        'just one finger, wield anything and silence anyone before they could scream".',

        'The Nimbleness, as in agility and dexterity, is a discipline that gave the Shadow Priests their name in the first '
        'place. The time spent in Nimbleness training indicates how fast the Priest can move, how good he can hide and '
        'how efficient he is picking the lock or searching trough other\'s pockets, whether the pocket\'s owner is dead, '
        'unconscious or alive and clueless. The supposed masters of this discipline can "merge themselves with the shadows '
        'to be never seen as mere mortals". ',

        'The Endurance, as in constitution and vim, is one of the primary disciplines, learned by Priests. The number of '
        'exhausting Endurance exercises undertaken indicates how much damage the Priest can survive, how he deals with blood loss, '
        'being poisoned, burned, frozen, crippled or touched by the powers and forces of the unknown(?). The supposed masters '
        'of this discipline can "survive a thousand arrows, a slit throat and a knife in the heart".',

        'The Advertence, as in observance and attention, is considered one of the basic disciplines learned by Priests. '
        'The extent of success in Advertence practice indicates how attentive and responsive to surroundings the Priest is, '
        'how far he sees or hears, how likely he is to spot the hidden passages, items, creatures or people. The supposed masters '
        'of this discipline can "spot a fly in a hundred miles, see inside the essence of darkness and witnesses anything, '
        'as the whole world is their eyes and ears".',

        'The Knowledge, as in intellect and wisdom is one of the most respected disciplines for the Priests. The achievements '
        'in Knowledge tuition indicates how intelligent the Priest is, how much he can learn from books, how good he can '
        'memorize the surroundings, how good he is at questioning someone and how much powers of the unknown(?) he can wield. '
        'There is no information that can unravel what supposed masters of this discipline can or cannot do. ',
    ]
    player_stats = MENU.values_pick_menu('PRIEST IS INITIATING', '                      Select your base stats:', val_names, descriptions, 1, 10, 4, 30)
    player = Player(0, 0)
    player.set_name(player_name)
    player.get_rpg_stats().set_stats_by_array(player_stats)
    return player

