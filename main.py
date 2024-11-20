import argparse
from setup import palette, streets
from server import server
from modes.mode import Mode
from config.config import Config
import os
import logging
import logging.handlers

from sources.forecast import ForecastProvider
from sources.mock_forecast import MockForecast
from sources.online_forecast import OnlineForecast
from state.state import State
from constants import paths

_logger = logging.getLogger(__name__)

def provider(mock: bool) -> ForecastProvider:
    if not mock:
        return OnlineForecast()
    
    return MockForecast()

def render_clear(mock: bool):
    Mode.Clear.run(State.instance(), provider(mock))


def render_storm(mock: bool):
    Mode.Storm.run(State.instance(), provider(mock))


def setup(_):
    create_data_dir()
    palette.create()
    streets.create()


def create_data_dir():
    if not paths.DATA_DIR.is_dir():
        _logger.info(f'{paths.DATA_DIR} missing, creating it')
        os.mkdir(paths.DATA_DIR)
    else:
        _logger.info(f'{paths.DATA_DIR} exists')


def run_server(_):
    setup(None)
    s = server.create()
    s.run()


def setup_logs():
    config = Config.instance()
    handler = logging.handlers.RotatingFileHandler('radar-frame.log',
                                                   maxBytes=100_000,
                                                   backupCount=4)
    
    handler.setFormatter(
        logging.Formatter('{asctime} {levelname} {name} {filename}:{lineno} {message}',
        style='{'))

    logging.basicConfig(
        handlers=[handler],
        level=logging.getLevelName(config['logging']['level']))


def create_server():
    """Helper to create a server to be used by Gunicorn."""
    setup_logs()
    setup(None)
    return server.create()


COMMANDS = {
    'setup': setup,
    'render-clear': render_clear,
    'render-storm': render_storm,
    'run-server': run_server,
}


def main():
    epilog = 'commands:\n'
    epilog += '\n'.join([f"  {c[0] + ':':<20}{c[1].__doc__}" for c in COMMANDS.items()])
    parser = argparse.ArgumentParser(
        usage='%(prog)s [COMMAND] [-d]',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=epilog
    )

    parser.add_argument('command', help=f'one of {", ".join(COMMANDS.keys())}')
    parser.add_argument('--mock', action='store_true', help='use mock forecast data')

    args = parser.parse_args()

    setup_logs()

    if args.command in COMMANDS:
        COMMANDS[args.command](args.mock)

    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
