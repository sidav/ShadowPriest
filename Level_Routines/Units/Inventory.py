from ..Items.Item import Item
from Message_Log import MessageLog as LOG

class Inventory:

    backpack = []

    equipped_weapon = None
    equipped_armor = None
    equipped_ammo = None

    def __init__(self):
        self.backpack = []

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

    def get_equipped_weapon(self):
        return self.equipped_weapon

    def get_equipped_armor(self):
        return self.equipped_armor

    def get_equipped_ammo(self):
        return self.equipped_weapon

    def get_backpack(self):
        return self.backpack

    def add_item_to_backpack(self, item):
        self.backpack.append(item)

    def remove_item_from_backpack(self, item):
        self.backpack.remove(item)
