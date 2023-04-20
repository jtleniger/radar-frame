import os
from PIL import Image
import logging
from config.config import Config

from constants import paths, radar, colors

_logger = logging.getLogger(__name__)


def _run_and_check(cmd):
    _logger.info('command:')
    _logger.info(cmd)

    exit_code = os.system(cmd)

    if exit_code != 0:
        raise Exception(f'exited {exit_code}')


def render():
    config = Config.instance()

    min_lat = config['bbox']['min_lat']
    min_lon = config['bbox']['min_lon']
    max_lat = config['bbox']['max_lat']
    max_lon = config['bbox']['max_lon']

    cmds = []
    
    # Convert raw data to georeferenced CSV
    cmd = f'{paths.NEXRAD_JSON_BIN} -o {paths.RADAR_JSON} {paths.RADAR_RAW}'
    cmds.append(cmd)

    # Rasterize
    cmd = 'gdal_rasterize -a value -ot byte -te '
    cmd += f'{min_lon} {min_lat} {max_lon} {max_lat} '
    cmd += f'-ts {radar.WIDTH} {radar.HEIGHT} '
    cmd += f'{paths.RADAR_JSON} {paths.RADAR_TIF}'
    cmds.append(cmd)

    # Colorize
    cmd = f'gdaldem color-relief {paths.RADAR_TIF} '
    cmd += f'gdal-colors.txt -alpha -nearest_color_entry {paths.RADAR_TIF}'
    cmds.append(cmd)

    # Convert to PNG
    cmd = f'gdal_translate -of PNG {paths.RADAR_TIF} {paths.RADAR_IMG}'
    cmds.append(cmd)

    for cmd in cmds:
        _run_and_check(cmd)

    image = Image.new('RGBA', (radar.WIDTH, radar.HEIGHT), colors.BLACK)
    radar_img = Image.open(paths.RADAR_IMG)
    streets = Image.open(paths.STREETS_IMG)
    image.paste(radar_img, (0, 0), radar_img)
    image.paste(streets, (0, 0), streets)
    image.save(paths.RADAR_IMG)