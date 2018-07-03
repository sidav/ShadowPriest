from Routines import SidavRandom as rand
from .Player.Player import Player
from .Items.Item import Item
from .Items.Potion import Potion
from .Items.Ammunition import Ammunition
from .Creators import ActorCreator as AC, WeaponCreator as WC
from Routines import SidavLOS as LOS


def initialize_level(lvl, player):
    placed_player_x, placed_player_y = place_player(lvl, player)
    # let's restrict spawning units in player LOS:
    opacity_map = lvl.get_opacity_map()
    vis_map_for_spawned_player = LOS.getVisibilityTableFromPosition(placed_player_x, placed_player_y, opacity_map, 15)
    # pass player LOS to unit placement routine as restriction map:
    place_random_units(lvl, vis_map_for_spawned_player)
    place_key_holders(lvl, vis_map_for_spawned_player)
    place_random_items(lvl)
    return lvl


def place_player(lvl, player):
    for posx in range(lvl.MAP_WIDTH):
        for posy in range(lvl.MAP_HEIGHT):
            if lvl.is_upstairs_present(posx, posy):
                player.set_coordinates(posx, posy)
                lvl._player = player
                lvl._player.get_inventory().equip_item(WC.create_dagger(posx, posy))
                lvl._player.get_inventory().add_item_to_backpack(Potion(posx, posy, 'Healing'))
                lvl._player.get_inventory().add_item_to_backpack(Potion(posx, posy, 'Healing'))
                lvl._player.get_inventory().add_item_to_backpack(Potion(posx, posy, 'PoIsOn'))
                lvl._player.get_inventory().add_item_to_backpack(Potion(posx, posy, 'POISON'))
                lvl._player.get_inventory().add_item_to_backpack(Potion(posx, posy, 'Painkiller'))
                lvl._player.get_inventory().add_item_to_backpack(Potion(posx, posy, 'Painkiller'))
                # lvl._player.get_inventory().add_item_to_backpack(WC.create_revolver(posx, posy))
                # lvl._player.get_inventory().add_item_to_backpack(Ammunition(0, 0, '9x19 hollow-point ammo', '9x19', (196, 64, 128), 13))
                return posx, posy


def place_random_units(lvl, restriction_map): 
    for _ in range(10):
        posx = posy = 0
        while not (lvl.is_tile_passable(posx, posy)) or restriction_map[posx][posy]:
            posx = rand.rand(lvl.MAP_WIDTH)
            posy = rand.rand(lvl.MAP_HEIGHT)
        unit = AC.create_guard(posx, posy, rand.rand(2))
        # unit.get_inventory().add_item_to_backpack(Item(posx, posy, name='Some debug item', color=(192, 0, 32)))
        lvl.spawn_unit(unit)


def place_key_holders(lvl, restriction_map):
    for lock in range(2): # <-- PLACEHOLDER! TODO: deal with it B-/
        for _ in range(get_number_of_keys_for_lock_level(lock+1)):
            posx = posy = 0
            while not (lvl.is_tile_passable(posx, posy)) or lvl.get_tile_lock_level(posx, posy) > lock \
                    or restriction_map[posx][posy]:
                posx = rand.rand(lvl.MAP_WIDTH)
                posy = rand.rand(lvl.MAP_HEIGHT)
            print("Keyholder added at {}, {}, key is {}".format(posx, posy, lock+1))
            unit = AC.create_key_holder(posx, posy, lock+1)
            lvl.spawn_unit(unit)


def place_random_items(lvl): # <- FUCKING TEMPORARY # TODO: REMOVE
    pass
    # # rand.randomize()
    # for lock in range(2): # <-- PLACEHOLDER! TODO: deal with it B-/
    #     posx = posy = 0
    #     while not (lvl.is_tile_passable(posx, posy)) or lvl.get_tile_lock_level(posx, posy) != lock:
    #         posx = rand.rand(lvl.MAP_WIDTH)
    #         posy = rand.rand(lvl.MAP_HEIGHT)
    #     print("Key added at {}, {}".format(posx, posy))
    #     lvl._items_on_floor.append(Key(posx, posy, lock+1))

    # for _ in range(15):
    #     weapon = WC.create_dagger(0, 0)
    #     place_item_at_random_coordinates(lvl, weapon)
    # for _ in range(15):
    #     weapon = WC.create_revolver(0, 0)
    #     place_item_at_random_coordinates(lvl, weapon)

    # for _ in range(15):
    #     ammo = Ammunition(0, 0, '9x19 ammo', '9x19', (196, 160, 64), 5)
    #     place_item_at_random_coordinates(lvl, ammo)
    # for _ in range(15):
    #     ammo = Ammunition(0, 0, '9x19 hollow-point ammo', '9x19', (196, 64, 128), 5)
    #     place_item_at_random_coordinates(lvl, ammo)
    # for _ in range(15):
    #     ammo = Ammunition(0, 0, 'poison dart', 'dart', (64, 128, 64), 5)
    #     place_item_at_random_coordinates(lvl, ammo)


def place_item_at_random_coordinates(lvl, item):
    posx = posy = 0
    while not (lvl.is_tile_passable(posx, posy)):
        posx = rand.rand(lvl.MAP_WIDTH)
        posy = rand.rand(lvl.MAP_HEIGHT)
    item.set_position(posx, posy)
    lvl._items_on_floor.append(item)


def get_number_of_keys_for_lock_level(lock_level):
    if lock_level == 1:
        return 2
    elif lock_level == 2:
        return 1
    else:
        return 0
