from dataclasses import dataclass
from datetime import datetime

@dataclass
class CurrentConditions:
    temp_f: float
    wind_mph: int
    code: int
    sunrise_local: datetime
    sunset_local: datetime

    def is_night(self, now_local: datetime):
        return now_local < self.sunrise_local or now_local > self.sunset_local