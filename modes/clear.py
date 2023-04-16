import logging

from sources import open_meteo
from views import clear

logger = logging.getLogger(__name__)

def run(state, config):
    res = open_meteo.get(open_meteo.Request.from_config())
    clear.render(config, res)
