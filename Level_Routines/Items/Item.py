import copy

class Item:
    _stackable = True
    _quantity = 1
    _appearance = '*'
    _color = (192, 192, 0)
    _name = 'Unknown Item'
    _pos_x, _pos_y = 0, 0
    _weight = 1

    def __init__(self, posx, posy, appearance='*', color=(192, 192, 0), name='Unknown Item', weight=1, stackable=True,
                 quantity=1):
        self._pos_x = posx
        self._pos_y = posy
        self._appearance = appearance
        self._color = color
        self._name = name
        self._weight = weight
        self._stackable = stackable
        if self._stackable:
            self._quantity = quantity

    def set_position(self, x, y):
        self._pos_x, self._pos_y = x, y

    def get_position(self):
        return self._pos_x, self._pos_y

    def is_stackable(self):
        return self._stackable

    def is_stackable_with(self, item):
        return self._stackable and item.get_singular_name() == self._name and self != item

    def pick_amount_from_stack(self, amount):
        to_return = None
        if self._stackable and self._quantity >= amount:
            to_return = copy.deepcopy(self)
            self.change_quantity_by(-amount)
            to_return.set_quantity(amount)
        return to_return

    def set_quantity(self, qty):
        self._quantity = qty

    def get_quantity(self):
        return self._quantity

    def change_quantity_by(self, qty):
        self._quantity += qty

    def get_singular_name(self):
        return self._name

    def get_name(self):
        if self._quantity != 1:
            return '{} {}s'.format(self._quantity, self._name)
        else:
            return self._name

    def is_of_type(self, type):
        return self.__class__.__name__ == type

    def get_color(self):
        return self._color

    def get_appearance(self):
        return self._appearance

    def is_body(self):
        return False
