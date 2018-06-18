class StatusEffect:

    def __init__(self, name, exp_turn):
        self._expiration_turn = exp_turn
        self._name = name

    def get_name(self):
        return self._name

    def get_expiration_turn(self):
        return self._expiration_turn
