import logging

from sources import open_meteo
from components.forecast.render import render as render_forecast
from views import clear

logger = logging.getLogger(__name__)

def run(state, config):
    res = open_meteo.get(open_meteo.Request.from_config())
    render_forecast(config, res)

    clear.render(config)
