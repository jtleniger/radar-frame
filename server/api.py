from http import HTTPStatus
from flask import Blueprint, send_file, Response, render_template, request
from datetime import datetime, timezone, timedelta
import logging

from modes.mode import Mode
from modes.mode_select import ModeSelect
from sources.online_forecast import OnlineForecast
from state.state import State
from sources import nws_api
from constants import paths

_logger = logging.getLogger(__name__)

api = Blueprint("api", __name__)


def _update_mode() -> bool:
    """Returns true if the mode changed."""
    state = State.instance()

    old_state = state.mode

    radar_status = nws_api.radar_status()

    _logger.info(radar_status)

    if not radar_status.up:
        _logger.error("radar down")
        state.mode = Mode.Clear
    elif radar_status.vcp == -1:
        _logger.error("some issue with nws api")
        state.mode = Mode.Clear
    elif radar_status.clear_air_mode():
        state.mode = Mode.Clear
    else:
        state.mode = Mode.Storm

    return state.mode != old_state


@api.route("/")
def index():
    state = State.instance()
    return render_template(
        "index.html",
        mode=state.mode.name,
        last_updated=state.get_last_updated_str(),
        mode_select=state.mode_select.name,
        manual_til=state.get_manual_til_str()
    )

@api.route("/settings", methods=['POST'])
def settings():
    _logger.debug(request.form)
    new_mode_select = ModeSelect[request.form['mode-select']]

    _logger.info(f'Set mode select to {new_mode_select}')

    state = State.instance()

    state.mode_select = new_mode_select

    old_mode = state.mode

    if state.mode_select == ModeSelect.Manual:
        state.manual_til = datetime.now(tz=timezone.utc) + timedelta(days=1)
    else:
        state.manual_til = None

    if state.mode_select == ModeSelect.Manual and 'mode' in request.form:
        state.mode = Mode[request.form['mode']]

    if old_mode != state.mode:
        state.last_updated = datetime(1970, 1, 1, tzinfo=timezone.utc)

    return render_template(
        "partials/settings.html",
        mode=state.mode.name,
        last_updated=state.get_last_updated_str(),
        mode_select=state.mode_select.name,
        manual_til=state.get_manual_til_str()
    )


@api.route("/frame")
def frame():
    debug = request.args.get("debug")

    if debug == "true":
        _logger.info("debug param set, sending current output")
        return send_file(paths.OUTPUT_IMG, mimetype="image/png")

    state = State.instance()

    now = datetime.now(tz=timezone.utc)

    _logger.info(f"last updated: {state.last_updated}")
    _logger.info(f"now: {now}")

    if state.mode_select == ModeSelect.Manual:
        if not state.manual_til or now > state.manual_til:
            state.mode_select = ModeSelect.Auto
            _logger.info('manual mode expired')

    if state.mode_select == ModeSelect.Auto:
        # If the state changed, reset the last updated timestamp.
        if _update_mode():
            state.last_updated = datetime(1970, 1, 1, tzinfo=timezone.utc)
    else:
        _logger.info('manual mode, maintaining state')

    if now > (state.last_updated + state.mode.interval()):
        state.run_mode(OnlineForecast())

        state.last_updated = now

        return send_file(paths.OUTPUT_IMG, mimetype="image/png")
    else:
        return Response(status=HTTPStatus.NOT_MODIFIED)
