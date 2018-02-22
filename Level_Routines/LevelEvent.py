
class LevelEvent:

    text = "empty event"

    visual = True

    acustic = True
    hear_radius = 3

    continious = False
    expiration_turn = 0

    def __init__(self, text, visual, hear_radius=0, expiration_turn = 0):
        self.text = text
        self.visual = visual
        self.acustic = hear_radius > 0
        self.hear_radius = hear_radius
        self.continious = expiration_turn > 0
        self.expiration_turn = expiration_turn
