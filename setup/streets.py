import logging
import os.path

from config.config import Config
from sources import osm
from constants import paths, radar

_logger = logging.getLogger(__name__)

def generate_png():
    config = Config.instance()

    min_lat = config['bbox']['min_lat']
    min_lon = config['bbox']['min_lon']
    max_lat = config['bbox']['max_lat']
    max_lon = config['bbox']['max_lon']

    cmd = 'gdal_rasterize --config OSM_USE_CUSTOM_INDEXING NO -te '
    cmd += f'{min_lon} {min_lat} {max_lon} {max_lat} '
    cmd += f'-ts {radar.WIDTH} {radar.HEIGHT} '
    cmd += '-burn 255 -ot byte -l lines -a_nodata 1 '
    cmd += f'{paths.STREETS_DATA} {paths.STREETS_TIF}'

    _logger.info('rasterize command:')
    _logger.info(cmd)

    exit_code = os.system(cmd)

    if exit_code != 0:
        ex = Exception('could not rasterize osm data')
        _logger.error(ex)
        raise ex
    
    cmd = f'gdal_translate -of PNG {paths.STREETS_TIF} {paths.STREETS_IMG}'

    _logger.info('convert to png command:')
    _logger.info(cmd)

    exit_code = os.system(cmd)

    if exit_code != 0:
        ex = Exception('could not rasterize osm data')
        _logger.error(ex)
        raise ex

def create():
    img_exists = paths.STREETS_IMG.exists()
    data_exists = paths.STREETS_DATA.exists()

    if img_exists:
        _logger.info(f'{paths.STREETS_IMG} already exists, doing nothing')
        return
    
    if data_exists and not img_exists:
        _logger.info(f'{paths.STREETS_DATA} exists, generating png')
        generate_png()
    
    if not data_exists:
        _logger.info(f'{paths.STREETS_DATA} missing, downloading data and generating png')
        osm.get()
        generate_png()
