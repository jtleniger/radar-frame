import logging

from sources import nexrad_level2, open_meteo
from components.radar.render import render as render_radar

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from state.state import State

from views import storm
from constants import paths

_logger = logging.getLogger(__name__)

def run(state: "State"):
    latest = nexrad_level2.latest_object()

    if latest and latest.last_modified > state.radar_last_updated:
        _logger.info(f'downloading {latest.key}')

        nexrad_level2.download(latest, to=str(paths.RADAR_RAW))

        state.radar_last_updated = latest.last_modified

        render_radar()
    else:
        _logger.info('using old radar data')

    current = open_meteo.current()
    hourly = open_meteo.hourly()

    storm.render(current, hourly)
