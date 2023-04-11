from datetime import datetime, timezone

from modes.mode import Mode

class State:
    _state = None

    def __init__(self):
        self.last_updated = datetime(1970, 1, 1, tzinfo=timezone.utc)
        self.radar_last_updated = datetime(1970, 1, 1, tzinfo=timezone.utc)
        self.mode = Mode.Storm

    def run_mode(self, config):
        self.mode.run(self, config)

    @staticmethod
    def instance():
        if State._state is None:
            State._state = State()

        return State._state