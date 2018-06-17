class RpgStats:
    # _strength = 5
    # _nimbleness = 5
    # _endurance = 5
    # _advertence = 5
    # _knowledge = 5

    def __init__(self, s=5, n=5, e=5, a=5, k=5):
        self._strength = s
        self._nimbleness = n
        self._endurance = e
        self._advertence = a
        self._knowledge = k

    def set_stats_by_array(self, array):
        self._strength = array[0]
        self._nimbleness = array[1]
        self._endurance = array[2]
        self._advertence = array[3]
        self._knowledge = array[4]

    def get_stats_array(self):
        return [
            self._strength,
            self._nimbleness,
            self._endurance,
            self._advertence,
            self._knowledge
        ]

    # def get_all_stats(self):
    def get_strength(self): 
        return self._strength

    def get_nimbleness(self):
        return self._nimbleness

    def get_endurance(self):
        return self._endurance

    def get_advertence(self):
        return self._advertence

    def get_knowledge(self):
        return self._knowledge

    def get_skill(self, skill):
        return 0
