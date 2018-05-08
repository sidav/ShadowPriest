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
        item_type = item.__class__.__name__
        if item_type == 'Weapon':
            self.add_item_to_backpack(self.equipped_weapon)
            self.equipped_weapon = item
        elif item_type == 'Armor':
            return
            pass
        elif item_type == 'Ammo':
            return
            pass
        else:
            LOG.append_error_message('attempt to equip the item of type "{}"'.format(item_type))
            return
        if item in self.backpack:
            self.remove_item_from_backpack(item)
        else:
            LOG.append_warning_message('equipping item not from backpack!')

    def remove_equipped_weapon(self):  # dangerous
        weapon = self.equipped_weapon
        self.equipped_weapon = None
        return weapon

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
        for item in self.backpack:
            if item.is_of_type('Key'):
                if item.is_of_key_level(lock_level):
                    return True
        return False

    def get_weapons_from_backpack(self):
        wpns = []
        for item in self.backpack:
            if item.__class__.__name__ == 'Weapon':
                wpns.append(item)
        return wpns

    def add_item_to_backpack(self, item):
        if item is not None:
            self.backpack.append(item)

    def remove_item_from_backpack(self, item):
        self.backpack.remove(item)
