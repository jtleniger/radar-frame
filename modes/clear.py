import logging

from sources import open_meteo
from views import clear

_logger = logging.getLogger(__name__)

def run(state):
    current = open_meteo.current()
    hourly = open_meteo.hourly()
    daily = open_meteo.daily()
    clear.render(current, hourly, daily)
