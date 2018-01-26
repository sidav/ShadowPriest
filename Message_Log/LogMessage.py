class LogMessage:

    text = "EMPTY"
    replaceable = False
    color = (200, 200, 200)

    def __init__(self, text, replaceable=False, color=(200, 200, 200)):
        self.text = text
        self.replaceable = replaceable
        self.color = color
