import logging
import requests

from config.config import Config
from constants import paths

_BASE_URL = 'https://overpass-api.de/api/interpreter'
_FILTER = '["highway"~"motorway|primary"]'

logger = logging.getLogger(__name__)


def get():
    config = Config.instance()

    min_lat = config['bbox']['min_lat']
    min_lon = config['bbox']['min_lon']
    max_lat = config['bbox']['max_lat']
    max_lon = config['bbox']['max_lon']

    overpass_query = f"""
    way{_FILTER}({min_lat},{min_lon},{max_lat},{max_lon});
    out body;
    >;
    out skel qt;
    """

    logger.info('executing overpass query:')
    logger.info(overpass_query)

    response = requests.post(_BASE_URL, data={'data': overpass_query})

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.text

    with open(paths.STREETS_DATA, 'w') as outfile:
        outfile.write(data)
        logger.info(f'saved osm data to {paths.STREETS_DATA}')
