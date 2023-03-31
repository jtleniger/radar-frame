from dataclasses import dataclass

@dataclass
class CurrentConditions:
    temp_f: float
    wind_mph: int
    code: int