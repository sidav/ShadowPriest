from Routines import SidavRandom as rand
from .Player.Player import Player
from .Items.Item import Item
from .Creators import ActorCreator as AC


def initialize_level(lvl):
    place_random_units(lvl)
    place_player(lvl)
    place_random_items(lvl)
    return lvl


def place_player(lvl):
    posx = posy = 0
    while not (lvl.is_tile_passable(posx, posy)):
        posx = rand.rand(lvl.MAP_WIDTH)
        posy = rand.rand(lvl.MAP_HEIGHT)
    lvl._player = Player(posx, posy)


def place_random_units(lvl): # <- FUCKING TEMPORARY # TODO: REMOVE
    # rand.randomize()
    for _ in range(10):
        posx = posy = 0
        while not (lvl.is_tile_passable(posx, posy)):
            posx = rand.rand(lvl.MAP_WIDTH)
            posy = rand.rand(lvl.MAP_HEIGHT)
        lvl.spawn_unit(AC.create_guard(posx, posy, rand.rand(2)))


def place_random_items(lvl): # <- FUCKING TEMPORARY # TODO: REMOVE
    # rand.randomize()
    for _ in range(20): # <-- PLACEHOLDER! TODO: deal with it B-/
        posx = posy = 0
        while not (lvl.is_tile_passable(posx, posy)):
            posx = rand.rand(lvl.MAP_WIDTH)
            posy = rand.rand(lvl.MAP_HEIGHT)
        num_of_items = rand.rand(3)+2  # <-- PLACEHOLDER! TODO: deal with it B-/
        for _ in range(num_of_items):
            lvl._items_on_floor.append(Item(posx, posy))
    for _ in range(20): # <-- PLACEHOLDER! TODO: deal with it B-/
        posx = posy = 0
        while not (lvl.is_tile_passable(posx, posy)):
            posx = rand.rand(lvl.MAP_WIDTH)
            posy = rand.rand(lvl.MAP_HEIGHT)
        num_of_items = rand.rand(3)+2  # <-- PLACEHOLDER! TODO: deal with it B-/
        for _ in range(num_of_items):
            lvl._items_on_floor.append(Item(posx, posy, name='Another unknown item', color=(192, 0, 32)))
    for _ in range(20): # <-- PLACEHOLDER! TODO: deal with it B-/
        posx = posy = 0
        while not (lvl.is_tile_passable(posx, posy)):
            posx = rand.rand(lvl.MAP_WIDTH)
            posy = rand.rand(lvl.MAP_HEIGHT)
        num_of_items = rand.rand(3)+2  # <-- PLACEHOLDER! TODO: deal with it B-/
        for _ in range(num_of_items):
            lvl._items_on_floor.append(Item(posx, posy, name='Slightly less unknown item', color=(0, 192, 32)))
