class EventsStack:

    _events = []

    def __init__(self):
        pass

    def push_event(self, event, expiration_turn=0):
        if expiration_turn != 0:
            event.expiration_turn = expiration_turn
        self._events.append(event)

    def get_active_events(self):
        return self._events

    def get_player_perceivable_events(self):
        events = []
        for event in self._events:
            if event.is_perceivable_by_player() and not event.was_already_perceived():
                events.append(event)
        return events

    def cleanup_events(self, current_turn):
        events_to_remove = []
        for event in self._events:
            if event.get_expiration_turn() <= current_turn:
                events_to_remove.append(event)
        for event in events_to_remove:
            self._events.remove(event)
