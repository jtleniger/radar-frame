from dataclasses import dataclass

@dataclass
class Day:
    day: str
    high_f: float
    low_f: float
    precip_sum: float
    wind: float
    code: int