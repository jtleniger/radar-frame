from forecast.current import CurrentConditions
from forecast.day import Day
from urllib.parse import urlencode
from urllib.request import urlopen
import json
from datetime import datetime
from pytz import timezone

BASE_PARAMS = {
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


def fetch(config):
    timezone_str = config['forecast']['timezone']
    local_tz = timezone(timezone_str)

    params = BASE_PARAMS
    params['latitude'] = config['forecast']['lat']
    params['longitude'] = config['forecast']['lon']
    params['forecast_days'] = config['forecast']['days']
    params['timezone'] = timezone_str

    response = urlopen(f"{config['forecast']['base_api_url']}{urlencode(BASE_PARAMS)}")

    if response.status != 200:
        raise response.msg

    data = json.loads(response.read())

    current = CurrentConditions(
        temp_f=data['current_weather']['temperature'],
        wind_mph=data['current_weather']['windspeed'],
        code=data['current_weather']['weathercode'],
        sunrise_local=local_tz.localize(datetime.fromisoformat(data['daily']['sunrise'][0])),
        sunset_local=local_tz.localize(datetime.fromisoformat(data['daily']['sunset'][0])))
    
    days = []

    for i in range(len(data['daily']['time'])):
        days.append(Day(
            day=datetime.strptime(data['daily']['time'][i], '%Y-%m-%d').strftime('%a').lower(),
            high_f=data['daily']['temperature_2m_max'][i],
            low_f=data['daily']['temperature_2m_min'][i],
            precip_sum=data['daily']['precipitation_sum'][i],
            wind=data['daily']['windspeed_10m_max'][i],
            code=data['daily']['weathercode'][i],
        ))
    
    days[0].day = 'today'

    return current, days
