from ..Units.Actor import Actor
from . import WeaponCreator as WPN_C
from ..Items.Key import Key
from ..Items.Ammunition import Ammunition
from ..Items.Potion import Potion
from Routines.SidavRandom import rand

# This whole file contains placeholders for now and needs to be tweaked.


def create_guard(x, y, rank):
    # weapon = WPN_C.create_dagger(x, y)  # TODO: create weapons individually
    if rank == 0:
        color = (160, 160, 160)
        weapon = WPN_C.create_club(x, y)
        name = 'Guard'
    if rank == 1:
        color = (176, 160, 0)
        weapon = WPN_C.create_dagger(x, y)
        name = 'Guard Officer'
    guard = Actor(x, y, 'G', color, name)
    guard.get_inventory().equip_item(weapon)
    if rand(4) == 0:
        guard.get_inventory().add_item_to_backpack(Potion(x, y, 'Potion of healing'))
    return guard


def create_key_holder(x, y, lock_level):  # temporary (hehe...)
    # weapon = WPN_C.create_dagger(x, y)
    weapon = WPN_C.create_revolver(x, y)
    if lock_level == 1:
        color = (32, 192, 32)
        name = 'Guard Leutenant'
    if lock_level == 2:
        color = (192, 32, 32)
        name = 'Guard Captain'
    keyholder = Actor(x, y, 'G', color, name)
    keyholder.get_inventory().equip_item(weapon)
    keyholder.get_inventory().add_item_to_backpack(Ammunition(x, y, '9x19 ammo', '9x19', (196, 64, 128), 12))
    keyholder.get_inventory().add_item_to_backpack(Key(x, y, lock_level))
    keyholder.get_inventory().add_item_to_backpack(Potion(x, y, 'Potion of healing'))
    return keyholder


def create_enforcer(x, y):
    color = (128, 32, 176)
    weapon = WPN_C.create_dagger(x, y)
    name = 'Enforcer'
    enforcer = Actor(x, y, 'E', color, name)
    enforcer.get_inventory().equip_item(weapon)
    enforcer.get_inventory().add_item_to_backpack(Potion(x, y, 'Potion of healing'))
    enforcer.get_inventory().add_item_to_backpack(Key(x, y, 1))
    enforcer.get_inventory().add_item_to_backpack(Key(x, y, 2))
    enforcer.get_rpg_stats().set_stats_by_array([9, 6, 8, 8, 4])
    enforcer._max_hitpoints = 120  # <- deprecated shit
    return enforcer
