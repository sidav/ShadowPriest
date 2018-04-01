
class Event:

    # text = "Empty event"

    pos_x = pos_y = 0

    visual = True
    text_when_seen = 'Empty seen text'

    acoustic = True
    text_when_heard = 'Empty heared text'
    hear_radius = 3

    is_perceivable_by_player = True

    # continious = False
    expiration_turn = 0

    def __init__(self, x, y, s_text='NULL_SEEN_EVENT', h_text='NULL_HEARD_EVENT', visual=True, hear_radius=3, expiration_turn = 0):
        self.pos_x = x
        self.pos_y = y
        self.text_when_seen = s_text
        self.text_when_heard = h_text
        self.visual = visual
        self.acoustic = hear_radius > 0
        self.hear_radius = hear_radius
        # self.continious = expiration_turn > 0
        self.expiration_turn = expiration_turn

    def get_expiration_turn(self):
        return self.expiration_turn

    def get_text_when_seen(self):
        return self.text_when_seen

    def get_text_when_heard(self):
        return self.text_when_heard

    def get_position(self):
        return self.pos_x, self.pos_y

    def get_hear_radius(self):
        return self.hear_radius
