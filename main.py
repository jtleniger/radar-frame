import argparse
import configparser
from frame import frame
from palette import palette
from server import server
import radar.osm
import radar.map
import radar.fetch
import forecast.render
import forecast.open_meteo
import pickle
import os
import logging
import logging.handlers


def render(config, dry_run: bool):
    """runs the full render process"""
    logging.info('rendering frame image')
    render_radar(config, dry_run)
    render_forecast(config, dry_run)
    combine_renders(config, dry_run)
    logging.info('done')


def render_radar(config, dry_run: bool):
    """renders an image from the latest radar data. if --dry-run is set, uses ./nexrad-test-data instead."""
    if not dry_run:
        latest = radar.fetch.latest_object(config)

        if not latest:
            logging.error('could not fetch latest radar data')
            return

        radar.fetch.fetch_radar(config, latest)

    radar.map.render_composite(config, dry_run)


def download_osm(config, dry_run: bool):
    """downloads OSM data. if --dry-run is passed, does nothing."""
    if not dry_run:
        radar.osm.download_data(config)


def render_forecast(config, dry_run: bool):
    """renders an image from the latest forecast data. if --dry-run is set, uses ./forecast-test-data instead."""
    if not dry_run:
        current_conditions, forecast_data = forecast.open_meteo.fetch(config)
    else:
        with open(config['files']['forecast_data_test'], 'rb') as infile:
            data = pickle.load(infile)

            current_conditions = data['current']
            forecast_data = data['forecast']

    forecast.render.render_image(
        config,
        current_conditions,
        forecast_data
    )


def combine_renders(config, _: bool):
    """creates a combined imaged from the outputs of render-radar and render-forecast"""
    frame.create(config)


def create_palette(config, _: bool):
    """creates the radar output color palette"""
    palette.create(config)


def create_data_dir(config):
    data_dir = config['files']['dir']

    if not os.path.isdir(data_dir):
        os.mkdir(data_dir)


def run_server(config, _: bool):
    s = server.create(config)
    s.run()


def get_config():
    config = configparser.ConfigParser()
    config.read('./config/config.ini')
    return config


def setup_logs(config):
    handler = logging.handlers.RotatingFileHandler(config['logging']['file'], maxBytes=100_000, backupCount=4)
    handler.setFormatter(logging.Formatter('{asctime} {levelname} {name} {filename}:{lineno} {message}', style='{'))

    logging.basicConfig(
        handlers=[handler],
        encoding='utf-8',
        level=logging.getLevelName(config['logging']['level']))


def create_server():
    """Helper to create a server to be used by Gunicorn."""
    config = get_config()
    setup_logs(config)
    return server.create(config)


COMMANDS = {
    'render': render,
    'render-radar': render_radar,
    'render-forecast': render_forecast,
    'combine-renders': combine_renders,
    'download-osm': download_osm,
    'create-palette': create_palette,
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
    parser.add_argument('-d', '--dry-run', action='store_true', help="don't download data, just use test data")

    args = parser.parse_args()

    config = get_config()
    setup_logs(config)

    create_data_dir(config)

    if args.command in COMMANDS:
        COMMANDS[args.command](config, args.dry_run)

    else:
        parser.print_usage()


if __name__ == "__main__":
    main()
