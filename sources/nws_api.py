from typing import List
from urllib.parse import urlencode
import requests
import re
from dataclasses import dataclass
import logging
from enum import Enum, auto
from datetime import datetime

from config.config import Config

_logger = logging.getLogger(__name__)

_BASE_URL = 'https://api.weather.gov/'


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


def alerts() -> List[Alert]:
    config = Config.instance()

    params = {
        'zone': f"{config['nws']['zone']},{config['nws']['fire_zone']}"
    }

    url = f"{_BASE_URL}alerts/active?{urlencode(params)}"

    _logger.info(url)

    response = requests.get(url, headers={'User-Agent': config['nws']['user_agent']})

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()

    return [Alert.from_dict(alert['properties']) for alert in data['features']]


def radar_status() -> RadarStatus:
    config = Config.instance()

    url = f"{_BASE_URL}radar/stations/{config['radar']['nexrad_id']}"

    _logger.info(url)

    response = requests.get(url, headers={'User-Agent': config['nws']['user_agent']})

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()

    raw_vcp = data['properties']['rda']['properties']['volumeCoveragePattern']

    vcp_match = re.search(r'[0-9]+', raw_vcp)

    if not vcp_match:
        vcp = -1
    else:
        vcp = int(vcp_match.group())

    status = data['properties']['rda']['properties']['status']

    up = status == 'Operate'

    return RadarStatus(up, vcp)
