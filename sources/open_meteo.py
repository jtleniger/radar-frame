import requests
from urllib.parse import urlencode
from pytz import timezone
from datetime import datetime, timezone as pytimezone
from typing import List
import logging
from sources import forecast

from config.config import Config

_logger = logging.getLogger(__name__)

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
    return forecast.CurrentConditions(
        temp_f=data['current_weather']['temperature'],
        code=data['current_weather']['weathercode'],
        is_day=data['current_weather']['is_day'] == 1)


def hourly() -> List[forecast.ForecastHour]:
    config = Config.instance()

    now_utc = datetime.now(tz=pytimezone.utc)
    local_tz = timezone(config['forecast']['timezone'])
    now_local = now_utc.astimezone(local_tz)
    ## todo: find nearest hour
    now_local_hour = now_local.replace(minute=0, second=0, microsecond=0)

    data = _get(_HOURLY_PARAMS.copy())

    hours = []

    for i in range(len(data['hourly']['time'])):
        time = datetime.fromisoformat(data['hourly']['time'][i])
        time = local_tz.localize(time)

        if time < now_local_hour:
            continue

        hours.append(forecast.ForecastHour(
            hour=time.strftime('%-I%p').lower(),
            temp_f=data['hourly']['temperature_2m'][i],
            code=data['hourly']['weathercode'][i],
        ))

    # hours[0].hour = 'now'

    return hours


def daily() -> List[forecast.ForecastDay]:
    data = _get(_DAILY_PARAMS.copy())

    days = []

    for i in range(len(data['daily']['time'])):
        days.append(forecast.ForecastDay(
            day=datetime
                .strptime(data['daily']['time'][i], '%Y-%m-%d')
                .strftime('%a').lower(),
            high_f=data['daily']['temperature_2m_max'][i],
            low_f=data['daily']['temperature_2m_min'][i],
            code=data['daily']['weathercode'][i],
        ))

    return days
