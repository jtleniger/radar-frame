from config.config import Config
from pytz import timezone
from datetime import datetime, timezone as pytimezone

from modes.mode import Mode

from typing import TYPE_CHECKING

from modes.mode_select import ModeSelect
if TYPE_CHECKING:
    from sources.forecast import ForecastProvider

class State:
    _state = None

    def __init__(self):
        self.last_updated = datetime(1970, 1, 1, tzinfo=pytimezone.utc)
        self.radar_last_updated = datetime(1970, 1, 1, tzinfo=pytimezone.utc)
        self.mode = Mode.Clear
        self.mode_select = ModeSelect.Auto
        self.manual_til: datetime | None = None

    def run_mode(self, forecast: "ForecastProvider"):
        self.mode.run(self, forecast)

    def get_last_updated_str(self):
        config = Config.instance()

        if self.last_updated == datetime(1970, 1, 1, tzinfo=pytimezone.utc):
            return None
        
        local_tz = timezone(config['forecast']['timezone'])
        last_updated_local = self.last_updated.astimezone(local_tz)
        
        return last_updated_local.strftime('%Y-%m-%d %I:%M%p')
    
    def get_manual_til_str(self):
        config = Config.instance()

        if not self.manual_til:
            return None
        
        local_tz = timezone(config['forecast']['timezone'])
        manual_til_local = self.manual_til.astimezone(local_tz)

        
        return manual_til_local.strftime('%Y-%m-%d %I:%M%p')

    @staticmethod
    def instance():
        if State._state is None:
            State._state = State()

        return State._state