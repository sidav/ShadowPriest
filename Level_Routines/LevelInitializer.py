from Routines import SidavRandom as rand
from .Player.Player import Player
from .Items.Item import Item
from .Creators import ActorCreator as AC, WeaponCreator as WC
from Routines import SidavLOS as LOS


def initialize_level(lvl):
    placed_player_x, placed_player_y = place_player(lvl)
    # let's restrict spawning units in player LOS:
    opacity_map = lvl.get_opacity_map()
    vis_map_for_spawned_player = LOS.getVisibilityTableFromPosition(placed_player_x, placed_player_y, opacity_map, 15)
    # pass player LOS to unit placement routine as restriction map:
    place_random_units(lvl, vis_map_for_spawned_player)
    place_random_items(lvl)
    return lvl


def place_player(lvl):
    for posx in range(lvl.MAP_WIDTH):
        for posy in range(lvl.MAP_HEIGHT):
            if lvl.is_upstairs_present(posx, posy):
                lvl._player = Player(posx, posy)
                lvl._player.get_inventory().equip_item(WC.create_dagger(posx, posy))
                return posx, posy


def place_random_units(lvl, restriction_map): 
    for _ in range(10):
        posx = posy = 0
        while not (lvl.is_tile_passable(posx, posy)) or restriction_map[posx][posy]:
            posx = rand.rand(lvl.MAP_WIDTH)
            posy = rand.rand(lvl.MAP_HEIGHT)
        unit = AC.create_guard(posx, posy, rand.rand(2))
        unit.get_inventory().add_item_to_backpack(Item(posx, posy, name='Some debug item', color=(192, 0, 32)))
        lvl.spawn_unit(unit)


def place_random_items(lvl): # <- FUCKING TEMPORARY # TODO: REMOVE
    # rand.randomize()
    for _ in range(10): # <-- PLACEHOLDER! TODO: deal with it B-/
        posx = posy = 0
        while not (lvl.is_tile_passable(posx, posy)):
            posx = rand.rand(lvl.MAP_WIDTH)
            posy = rand.rand(lvl.MAP_HEIGHT)
        num_of_items = rand.rand(3)+2  # <-- PLACEHOLDER! TODO: deal with it B-/
        for _ in range(num_of_items):
            lvl._items_on_floor.append(Item(posx, posy))
    for _ in range(10): # <-- PLACEHOLDER! TODO: deal with it B-/
        posx = posy = 0
        while not (lvl.is_tile_passable(posx, posy)):
            posx = rand.rand(lvl.MAP_WIDTH)
            posy = rand.rand(lvl.MAP_HEIGHT)
        num_of_items = rand.rand(3)+2  # <-- PLACEHOLDER! TODO: deal with it B-/
        for _ in range(num_of_items):
            lvl._items_on_floor.append(Item(posx, posy, name='Another unknown item', color=(192, 0, 32)))
    for _ in range(10): # <-- PLACEHOLDER! TODO: deal with it B-/
        posx = posy = 0
        while not (lvl.is_tile_passable(posx, posy)):
            posx = rand.rand(lvl.MAP_WIDTH)
            posy = rand.rand(lvl.MAP_HEIGHT)
        num_of_items = rand.rand(3)+2  # <-- PLACEHOLDER! TODO: deal with it B-/
        for _ in range(num_of_items):
            lvl._items_on_floor.append(Item(posx, posy, name='Slightly less unknown item', color=(0, 192, 32)))
    for _ in range(20): # <-- PLACEHOLDER! TODO: deal with it B-/
        posx = posy = 0
        while not (lvl.is_tile_passable(posx, posy)):
            posx = rand.rand(lvl.MAP_WIDTH)
            posy = rand.rand(lvl.MAP_HEIGHT)
        num_of_items = rand.rand(3)+2  # <-- PLACEHOLDER! TODO: deal with it B-/
        for _ in range(num_of_items):
            weapon = WC.create_dagger(posx, posy)
            lvl._items_on_floor.append(weapon)
