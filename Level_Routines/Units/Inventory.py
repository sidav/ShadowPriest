from ..Items.Item import Item
from Message_Log import MessageLog as LOG

class Inventory:

    backpack = []

    equipped_weapon = None
    equipped_armor = None
    equipped_ammo = None
    body_on_shoulder = None

    def __init__(self):
        self.backpack = []
        self.equipped_weapon = None
        self.equipped_armor = None
        self.equipped_ammo = None
        # self.key_ring = []  <--- maybe later
        self.body_on_shoulder = None

    def count_total_weight(self):
        wght = 0
        for item in self.backpack:
            wght += item._weight
        return wght

    def equip_item(self, item):  # TODO: consider working with items through Unit methods?
        if item.is_of_type('Weapon'):
            self.add_item_to_backpack(self.equipped_weapon)
            self.equipped_weapon = item
        elif item.is_of_type('Armor'):
            return
            pass
        elif item.is_of_type('Ammunition'):
            self.add_item_to_backpack(self.equipped_ammo)
            self.equipped_ammo = item
        else:
            LOG.append_error_message('attempt to equip the item of type "{}"'.format(item.__class__.__name__))
            return
        if item in self.backpack:
            self.remove_item_from_backpack(item)
        else:
            LOG.append_warning_message('equipping item not from backpack!')

    def remove_equipped_weapon(self):  # dangerous
        weapon = self.equipped_weapon
        self.equipped_weapon = None
        return weapon

    def remove_equipped_ammo(self):
        ammo_count = self.equipped_ammo.get_quantity()
        ammo = self.equipped_ammo if ammo_count > 0 else None  # dangerous
        self.equipped_ammo = None
        return ammo

    def move_weapon_to_backpack(self):
        self.add_item_to_backpack(self.equipped_weapon)
        self.equipped_weapon = None

    # def unequip_item(self, item_type_name):
    #     if item is None:
    #         LOG.append_error_message('Unequipping NoneType object!')
    #     item_type = item.__class__.__name__
    #     if item_type == 'Weapon':
    #         self.add_item_to_backpack(self.equipped_weapon)
    #         self.equipped_weapon = None
    #     elif item_type == 'Armor':
    #         return
    #         pass
    #     elif item_type == 'Ammo':
    #         return
    #         pass
    #     else:
    #         LOG.append_error_message('attempt to unequip the item of type "{}"'.format(item_type))
    #         return

    def get_equipped_weapon(self):
        return self.equipped_weapon

    def get_equipped_armor(self):
        return self.equipped_armor

    def get_equipped_ammo(self):
        return self.equipped_ammo

    def empty_equipped_ammo(self):
        self.equipped_ammo = None

    def get_body_on_shoulder(self):
        return self.body_on_shoulder

    def pick_body_on_shoulder(self, item):
        if self.body_on_shoulder is not None:
            LOG.append_error_message('Shoulder is not empty!')
            return
        self.body_on_shoulder = item

    def is_carrying_body_on_shoulder(self):
        return self.body_on_shoulder is not None

    def remove_body_from_shoulder(self):
        item = self.body_on_shoulder
        self.body_on_shoulder = None
        return item

    def get_backpack(self):
        return self.backpack

    def is_backpack_empty(self):
        return len(self.backpack) == 0

    def has_key_of_lock_level(self, lock_level):
        if lock_level == 0:
            # LOG.append_warning_message('attempt to request a key of zero lock level.')
            return True
        for item in self.backpack:
            if item.is_of_type('Key'):
                if item.is_of_key_level(lock_level):
                    return True
        return False

    def get_weapons_from_backpack(self):
        wpns = []
        for item in self.backpack:
            if item.is_of_type('Weapon'):
                wpns.append(item)
        return wpns

    def get_ammunition_from_backpack(self):
        ammo = []
        for item in self.backpack:
            if item.is_of_type('Ammunition'):
                ammo.append(item)
        return ammo

    def get_items_of_type_from_backpack(self, type):
        items = []
        for item in self.backpack:
            if item.is_of_type(type):
                items.append(item)
        return items

    def add_item_to_backpack(self, item):
        if item is not None:
            if item.is_of_type('Ammunition'):
                if self.equipped_ammo is None:
                    self.equip_item(item)
                    return
                elif self.equipped_ammo.is_stackable_with(item):
                    self.equipped_ammo.change_quantity_by(item.get_quantity())
                    return
            self.backpack.append(item)
            if item.is_stackable():
                self.try_stack_items_in_backpack()

    def remove_item_from_backpack(self, item):
        self.backpack.remove(item)

    def try_stack_items_in_backpack(self):
        items = self.backpack
        items_count = len(items)
        stack_successful = False
        if items_count > 1:  # then attempt to stack those items
            for i in range(items_count):
                for j in range(i, items_count):
                    if items[i].is_stackable_with(items[j]):
                        items[i].change_quantity_by(items[j].get_quantity())
                        self.remove_item_from_backpack(items[j])
                        stack_successful = True
                items = self.backpack
                items_count = len(items)
        return stack_successful
