from http import HTTPStatus
from flask import Blueprint, send_file, Response
from config.config import Config
from datetime import datetime, timezone
import logging

from modes.mode import Mode
from state.state import State
from sources import nws_api

logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)


@api.route('/frame')
def frame():
    state = State.instance()

    radar_status = nws_api.radar_status()

    logger.info(radar_status)

    if not radar_status.up:
        # TODO
        logger.error('radar down')

    if radar_status.vcp == -1:
        # TODO
        logger.error('some issue with nws api')

    if radar_status.clear_air_mode():
        state.mode = Mode.Clear
    else:
        state.mode = Mode.Storm

    now = datetime.now(tz=timezone.utc)

    if now > (state.last_updated + state.mode.interval()):
        state.run_mode(Config.instance())

        state.last_updated = now

        return send_file(Config.instance()['files']['output_img'], mimetype='image/png')
    else:
        return Response(status=HTTPStatus.NOT_MODIFIED)
