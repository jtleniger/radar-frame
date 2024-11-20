from sources.forecast import ForecastProvider
from views import clear

def run(forecast: ForecastProvider):
    current = forecast.current()
    hourly = forecast.hourly()
    daily = forecast.daily()
    alerts = forecast.alerts()
    clear.render(current, hourly, daily, alerts)
