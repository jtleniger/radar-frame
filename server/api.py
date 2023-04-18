from http import HTTPStatus
from flask import Blueprint, send_file, Response, jsonify
from datetime import datetime, timezone
import logging

from modes.mode import Mode
from state.state import State
from sources import nws_api
from constants import paths

_logger = logging.getLogger(__name__)

api = Blueprint('api', __name__)


def _update_mode() -> bool:
    """Returns true if the mode changed."""
    state = State.instance()

    old_state = state.mode

    radar_status = nws_api.radar_status()

    _logger.info(radar_status)

    if not radar_status.up:
        _logger.error('radar down')
        state.mode = Mode.Clear
    elif radar_status.vcp == -1:
        _logger.error('some issue with nws api')
        state.mode = Mode.Clear
    elif radar_status.clear_air_mode():
        state.mode = Mode.Clear
    else:
        state.mode = Mode.Storm

    return state.mode != old_state


@api.route('/frame')
def frame():
    state = State.instance()

    now = datetime.now(tz=timezone.utc)

    _logger.info(f'last updated: {state.last_updated}')
    _logger.info(f'now: {now}')

    # If the state changed, reset the last updated timestamp.
    if _update_mode():
        state.last_updated = datetime(1970, 1, 1, tzinfo=timezone.utc)

    if now > (state.last_updated + state.mode.interval()):
        state.run_mode()

        state.last_updated = now

        return send_file(paths.OUTPUT_IMG, mimetype='image/png')
    else:
        return Response(status=HTTPStatus.NOT_MODIFIED)
