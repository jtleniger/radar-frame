from typing import List
from urllib.parse import urlencode
import requests
import re
import logging
from sources import forecast

from config.config import Config

_logger = logging.getLogger(__name__)

_BASE_URL = 'https://api.weather.gov/'

def alerts() -> List[forecast.Alert]:
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

    return [forecast.Alert.from_dict(alert['properties']) for alert in data['features']]


def radar_status() -> forecast.RadarStatus:
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

    return forecast.RadarStatus(up, vcp)
