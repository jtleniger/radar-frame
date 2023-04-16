from urllib.parse import urlencode
from urllib.request import urlopen
import json
from datetime import datetime
from pytz import timezone
from dataclasses import dataclass
from typing import List

from config.config import Config


@dataclass
class CurrentConditions:
    temp_f: float
    wind_mph: int
    code: int
    sunrise_local: datetime
    sunset_local: datetime

    def is_night(self, now_local: datetime):
        return now_local < self.sunrise_local or now_local > self.sunset_local


@dataclass
class ForecastDay:
    day: str
    high_f: float
    low_f: float
    precip_sum: float
    wind: float
    code: int


@dataclass
class Forecast:
    days: List[ForecastDay]


@dataclass
class Request:
    timezone: str
    latitude: float
    longitude: float
    days: int

    @staticmethod
    def from_config():
        config = Config.instance()
        return Request(
            timezone=config['forecast']['timezone'],
            latitude=float(config['forecast']['lat']),
            longitude=float(config['forecast']['lon']),
            days=5
        )


@dataclass
class Response:
    current_conditions: CurrentConditions
    forecast: Forecast


_BASE_PARAMS = {
    'daily': ','.join([
        'weathercode',
        'temperature_2m_max',
        'temperature_2m_min',
        'precipitation_sum',
        'windspeed_10m_max',
        'sunrise',
        'sunset'
    ]),
    'current_weather': 'true',
    'temperature_unit': 'fahrenheit',
    'windspeed_unit': 'mph',
    'precipitation_unit': 'inch'
}

_BASE_URL = 'https://api.open-meteo.com/v1/forecast?'


def get(req: Request) -> Response:
    local_tz = timezone(req.timezone)

    params = _BASE_PARAMS
    params['latitude'] = str(req.latitude)
    params['longitude'] = str(req.longitude)
    params['forecast_days'] = str(req.days)
    params['timezone'] = req.timezone

    response = urlopen(f"{_BASE_URL}{urlencode(_BASE_PARAMS)}")

    if response.status != 200:
        raise Exception(response.msg)

    data = json.loads(response.read())

    current = CurrentConditions(
        temp_f=data['current_weather']['temperature'],
        wind_mph=data['current_weather']['windspeed'],
        code=data['current_weather']['weathercode'],
        sunrise_local=local_tz.localize(datetime.fromisoformat(data['daily']['sunrise'][0])),
        sunset_local=local_tz.localize(datetime.fromisoformat(data['daily']['sunset'][0])))

    forecast = Forecast([])

    for i in range(len(data['daily']['time'])):
        forecast.days.append(ForecastDay(
            day=datetime.strptime(data['daily']['time'][i], '%Y-%m-%d').strftime('%a').lower(),
            high_f=data['daily']['temperature_2m_max'][i],
            low_f=data['daily']['temperature_2m_min'][i],
            precip_sum=data['daily']['precipitation_sum'][i],
            wind=data['daily']['windspeed_10m_max'][i],
            code=data['daily']['weathercode'][i],
        ))

    forecast.days[0].day = 'today'

    return Response(current, forecast)
