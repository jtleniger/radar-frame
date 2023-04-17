from typing import List
import requests
import re
from dataclasses import dataclass
import logging

from config.config import Config

_logger = logging.getLogger(__name__)

_BASE_URL = 'https://api.weather.gov/'


@dataclass
class RadarStatus:
    up: bool
    vcp: int

    def clear_air_mode(self):
        return self.vcp in [31, 32, 35]


def alerts() -> List[str]:
    config = Config.instance()

    url = f"{_BASE_URL}alerts/active/zone/{config['nws']['zone']}"

    _logger.info(url)

    response = requests.get(url, headers={'User-Agent': config['nws']['user_agent']})

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()

    return [ alert['event'].lower() for alert in data['features'] ]


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
