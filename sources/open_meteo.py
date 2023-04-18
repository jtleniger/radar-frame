import requests
from urllib.parse import urlencode
from pytz import timezone
from datetime import datetime, timezone as pytimezone
from dataclasses import dataclass
from typing import List
import logging

from config.config import Config

_logger = logging.getLogger(__name__)


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


_CURRENT_PARAMS = {
    'current_weather': 'true',
    'temperature_unit': 'fahrenheit'
}

_DAILY_PARAMS = {
    'daily': ','.join([
        'weathercode',
        'temperature_2m_max',
        'temperature_2m_min',
    ]),
    'temperature_unit': 'fahrenheit',
    'forecast_days': 7
}

_HOURLY_PARAMS = {
    'hourly': ','.join([
        'weathercode',
        'temperature_2m'
    ]),
    'temperature_unit': 'fahrenheit',
    'forecast_days': 2
}

_BASE_URL = 'https://api.open-meteo.com/v1/forecast?'


def _get(params):
    config = Config.instance()

    params['latitude'] = config['forecast']['lat']
    params['longitude'] = config['forecast']['lon']
    params['timezone'] = config['forecast']['timezone']

    url = f"{_BASE_URL}{urlencode(params)}"
    _logger.info(f'url: {url}')
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()


def current():
    data = _get(_CURRENT_PARAMS.copy())
    return CurrentConditions(
        temp_f=data['current_weather']['temperature'],
        code=data['current_weather']['weathercode'],
        is_day=data['current_weather']['is_day'] == 1)


def hourly():
    config = Config.instance()

    now_utc = datetime.now(tz=pytimezone.utc)
    local_tz = timezone(config['forecast']['timezone'])
    now_local = now_utc.astimezone(local_tz)
    now_local_hour = now_local.replace(minute=0, second=0, microsecond=0)

    data = _get(_HOURLY_PARAMS.copy())

    forecast = []

    for i in range(len(data['hourly']['time'])):
        if len(forecast) > 4:
            break

        time = datetime.fromisoformat(data['hourly']['time'][i])
        time = local_tz.localize(time)

        if time < now_local_hour:
            continue

        forecast.append(ForecastHour(
            hour=time.strftime('%-I%p').lower(),
            temp_f=data['hourly']['temperature_2m'][i],
            code=data['hourly']['weathercode'][i],
        ))

    forecast[0].hour = 'now'

    return forecast


def daily() -> List[ForecastDay]:
    data = _get(_DAILY_PARAMS.copy())

    forecast = []

    for i in range(len(data['daily']['time'])):
        forecast.append(ForecastDay(
            day=datetime
                .strptime(data['daily']['time'][i], '%Y-%m-%d')
                .strftime('%a').lower(),
            high_f=data['daily']['temperature_2m_max'][i],
            low_f=data['daily']['temperature_2m_min'][i],
            code=data['daily']['weathercode'][i],
        ))

    return forecast
