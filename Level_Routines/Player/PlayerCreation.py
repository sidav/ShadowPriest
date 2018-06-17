import SidavMenu as MENU
from .Player import Player


def create_player():

    player_name = MENU.keyboard_input_menu('PRIEST IS INITIATING', 'What is your name, Priest?', 3, 25)

    val_names = ['Strength', 'Nimbleness', 'Endurance', 'Advertence', 'Knowledge']
    descriptions = [
        "Strength is all-around useful characteristic of the Priest. It represents how strong the shadow priest is, "
        "how powerful his melee attacks are, how much stuff he can carry and what kind of weapons he could use. "
        "The priest with high strength can wield heavy and powerful weapons, strangle enemies quicker, fights in melee"
        " more efficiently and isn't slowed down while carrying a lot of items in his inventory or a body on his shoulder.",

        "Nimbleness stat represents how quick and agile the shadow priest is, how fast he can move, how efficient he is while stabbing, "
        "picking the lock or searching trough other's pockets, whether the pocket's owner is dead, unconscious or alive and clueless. "
        "The one should be as nimble as strong to become a real Priest.",

        "Endurance stat represents how healthy and durable the shadow priest is, how much damage he can survive, "
        "how he deals with blood loss, being poisoned, burned, frozen, crippled or touched by the powers and forces "
        "of the unknown. They say that the Priest could endure very unsettling and hostile environment conditions for a very long time.",

        "Advertence stat represents how attentive and responsive to surroundings the shadow priest is, how far he sees or hears,"
        " how likely he is to spot the hidden passages, items, creatures or people. The rumors are that the experienced Priest "
        "is extraordinarily perceptive.",

        "Knowledge stat represents how intelligent the shadow priest is, how much he can learn from books, how good he can "
        "memorize the surroundings, how good he is at questioning someone and how much powers of the unknown he can wield.",
    ]
    player_stats = MENU.values_pick_menu('PRIEST IS INITIATING', 'Select your base stats:', val_names, descriptions, 1, 10, 4, 20)
    player = Player(0, 0)
    player.set_name(player_name)
    player.get_rpg_stats().set_stats_by_array(player_stats)
    return player

