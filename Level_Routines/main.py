from .Controllers import LevelController as LC
from .Player import PlayerCreation as PC

def init():
    player = PC.create_player()
    LC.initialize(player)

def start_main_loop():
    LC.control()