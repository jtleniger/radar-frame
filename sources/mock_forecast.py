from sources import forecast
from typing import List

class MockForecast(forecast.ForecastProvider):
    @staticmethod
    def current() -> forecast.CurrentConditions:
        return forecast.CurrentConditions(
            101.0,
            57,
            False
        )

    @staticmethod
    def hourly() -> List[forecast.ForecastHour]:
        return [
            forecast.ForecastHour('9pm', 24.0, 3),
            forecast.ForecastHour('10pm', 24.0, 50),
            forecast.ForecastHour('11pm', 24.0, 53),
            forecast.ForecastHour('12am', 24.0, 95),
            forecast.ForecastHour('1am', 124.0, 77),
            forecast.ForecastHour('2am', 24.0, 95),
            forecast.ForecastHour('3am', 124.0, 77),
            forecast.ForecastHour('4am', 24.0, 95),
            forecast.ForecastHour('5am', 124.0, 77)
        ]

    @staticmethod
    def daily() -> List[forecast.ForecastDay]:
        return [
            forecast.ForecastDay('tue', 38.8, 123.2, 1),
            forecast.ForecastDay('wed', 112.3, -25, 2),
            forecast.ForecastDay('thu', 38.8, 12.2, 3),
            forecast.ForecastDay('fri', 38.8, 123.2, 45),
            forecast.ForecastDay('tue', 38.8, 123.2, 53),
            forecast.ForecastDay('tue', 38.8, 123.2, 66),
            forecast.ForecastDay('tue', 38.8, 123.2, 77),
            forecast.ForecastDay('tue', 38.8, 123.2, 66),
            forecast.ForecastDay('tue', 38.8, 123.2, 77)
        ]

    @staticmethod
    def alerts() -> List[forecast.Alert]:
        return []

    @staticmethod
    def radar_status() -> forecast.RadarStatus:
        return forecast.RadarStatus(True, 31)