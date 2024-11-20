from sources import forecast
from sources import open_meteo
from sources import nws_api
from typing import List

class OnlineForecast(forecast.ForecastProvider):
    @staticmethod
    def current() -> forecast.CurrentConditions:
        return open_meteo.current()

    @staticmethod
    def hourly() -> List[forecast.ForecastHour]:
        return open_meteo.hourly()

    @staticmethod
    def daily() -> List[forecast.ForecastDay]:
        return open_meteo.daily()

    @staticmethod
    def alerts() -> List[forecast.Alert]:
        return nws_api.alerts()

    @staticmethod
    def radar_status() -> forecast.RadarStatus:
        return nws_api.radar_status()