import logging

from sources import nexrad_level2, open_meteo
from components.radar.render import render as render_radar
from views import storm
from constants import paths

logger = logging.getLogger(__name__)

def run(state, config):
    latest = nexrad_level2.latest_object()

    if latest and latest.last_modified > state.radar_last_updated:
        logger.info(f'downloading {latest.key}')

        nexrad_level2.download(latest, to=str(paths.RADAR_RAW))

        state.radar_last_updated = latest.last_modified

        render_radar(config, False)
    else:
        logger.info('using old radar data')

    res = open_meteo.get(open_meteo.Request.from_config())
    # render_forecast(config, res)

    storm.render(config)
