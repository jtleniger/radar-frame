from datetime import datetime
from dataclasses import dataclass
from typing import List
from enum import Enum, auto
from abc import ABC, abstractmethod

@dataclass
class CurrentConditions:
    temp_f: float
    code: int
    is_day: bool


@dataclass
class ForecastDay:
    day: str
    high_f: float
    low_f: float
    code: int


@dataclass
class ForecastHour:
    hour: str
    temp_f: float
    code: int


@dataclass
class RadarStatus:
    up: bool
    vcp: int

    def clear_air_mode(self):
        return self.vcp in [31, 32, 35]


class AlertLevel(Enum):
    Info = auto()
    Watch = auto()
    Warning = auto()
    Emergency = auto()

@dataclass
class Alert:
    event: str
    level: AlertLevel
    status: str
    effective: datetime
    expires: datetime

    @staticmethod
    def from_dict(alert):
        urgency = alert['urgency'].lower()
        severity = alert['severity'].lower()
        certainty = alert['certainty'].lower()

        if (urgency == 'future' and
            severity in ['extreme', 'severe', 'moderate']
            and certainty == 'possible'):

            level = AlertLevel.Watch

        elif (urgency in ['immediate', 'expected'] and
              certainty in ['likely', 'observed'] and
              severity in ['extreme', 'severe']):
            
            if severity == 'extreme':
                level = AlertLevel.Emergency
            else:
                level = AlertLevel.Warning
        else:
            level = AlertLevel.Info

        return Alert(
            event=alert['event'].lower(),
            level=level,
            status=alert['status'].lower(),
            effective=datetime.fromisoformat(alert['effective']),
            expires=datetime.fromisoformat(alert['expires'])       
        )

class ForecastProvider(ABC):
    @abstractmethod
    def current() -> CurrentConditions:
        raise NotImplementedError

    @abstractmethod
    def hourly() -> List[ForecastHour]:
        raise NotImplementedError

    @abstractmethod
    def daily() -> List[ForecastDay]:
        raise NotImplementedError

    @abstractmethod
    def alerts() -> List[Alert]:
        raise NotImplementedError

    @abstractmethod
    def radar_status() -> RadarStatus:
        raise NotImplementedError