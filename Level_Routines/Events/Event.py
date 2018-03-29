
class Event:

    # text = "Empty event"

    visual = True
    text_when_seen = 'Empty seen text'

    acoustic = True
    text_when_heard = 'Empty heared text'
    hear_radius = 3

    is_perceivable_by_player = True

    # continious = False
    expiration_turn = 0

    def __init__(self, s_text='NULL_SEEN_EVENT', h_text='NULL_HEARD_EVENT', visual=True, acoustic=True, hear_radius=3, expiration_turn = 0):
        self.text_when_seen = s_text
        self.text_when_heard = h_text
        self.visual = visual
        self.acoustic = hear_radius > 0
        self.hear_radius = hear_radius
        # self.continious = expiration_turn > 0
        self.expiration_turn = expiration_turn

    def get_expiration_turn(self):
        return self.expiration_turn

    def get_text(self):
        return self.text_when_seen
