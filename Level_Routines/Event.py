
class Event:

    text = "Empty event"

    visual = True

    acustic = True
    hear_radius = 3

    is_perceivable_by_player = True

    continious = False
    expiration_turn = 0

    def __init__(self, text, visual, hear_radius=0, expiration_turn = 0):
        self.text = text
        self.visual = visual
        self.acustic = hear_radius > 0
        self.hear_radius = hear_radius
        self.continious = expiration_turn > 0
        self.expiration_turn = expiration_turn

    def get_expiration_turn(self):
        return self.expiration_turn

    def get_text(self):
        return self.text
