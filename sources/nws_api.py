from urllib.request import Request, urlopen
import json
from dataclasses import dataclass
import re

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

    req = Request(f"{_BASE_URL}radar/stations/{config['radar']['nexrad_id']}")
    req.add_header('User-Agent', config['nws']['user_agent'])

    response = urlopen(req)

    if response.status != 200:
        raise response.msg

    data = json.loads(response.read())

    raw_vcp = data['properties']['rda']['properties']['volumeCoveragePattern']

    vcp_match = re.search(r'[0-9]+', raw_vcp)

    if not vcp_match:
        vcp = -1
    else:
        vcp = int(vcp_match.group())

    status = data['properties']['rda']['properties']['status']

    up = status == 'Operate'

    return RadarStatus(up, vcp)
