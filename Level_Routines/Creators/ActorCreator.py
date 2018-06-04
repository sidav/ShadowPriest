from ..Units.Actor import Actor
from . import WeaponCreator as WPN_C
from ..Items.Key import Key
from ..Items.Ammunition import Ammunition
from Routines.SidavRandom import rand

# This whole file contains placeholders for now and needs to be tweaked.


def create_guard(x, y, rank):
    weapon = WPN_C.create_dagger(x, y)  # TODO: create weapons individually
    if rank == 0:
        color = (160, 160, 160)
        name = 'Guard'
    if rank == 1:
        color = (176, 160, 0)
        name = 'Guard Officer'
    guard = Actor(x, y, 'G', color, name)
    guard.get_inventory().equip_item(weapon)
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
    return keyholder
