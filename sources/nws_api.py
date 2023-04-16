import requests
import json
import re
from dataclasses import dataclass

from config.config import Config

_BASE_URL = 'https://api.weather.gov/'


@dataclass
class RadarStatus:
    up: bool
    vcp: int

    def clear_air_mode(self):
        return self.vcp in [31, 32, 35]


def radar_status():
    config = Config.instance()

    url = f"{_BASE_URL}radar/stations/{config['radar']['nexrad_id']}"
    
    response = requests.get(url, headers={'User-Agent': config['nws']['user_agent']})

    if response.status_code != 200:
        raise Exception(response.text)

    data = json.loads(response.json())

    raw_vcp = data['properties']['rda']['properties']['volumeCoveragePattern']

    vcp_match = re.search(r'[0-9]+', raw_vcp)

    if not vcp_match:
        vcp = -1
    else:
        vcp = int(vcp_match.group())

    status = data['properties']['rda']['properties']['status']

    up = status == 'Operate'

    return RadarStatus(up, vcp)
