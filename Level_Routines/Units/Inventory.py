from ..Items.Item import Item

class Inventory:

    backpack = []

    equipped_weapon = None
    equipped_armor = None
    equipped_ammo = None

    def count_total_weight(self):
        wght = 0
        for item in self.backpack:
            wght += item._weight
        return wght

    def get_equipped_weapon(self):
        return self.equipped_weapon

    def get_equipped_armor(self):
        return self.equipped_armor

    def get_equipped_ammo(self):
        return self.equipped_weapon

    def get_backpack(self):
        return self.backpack

    def add_item(self, item):
        self.backpack.append(item)

    def remove_item(self, item):
        self.backpack.remove(item)
