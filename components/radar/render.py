import subprocess
from PIL import Image
import logging
from config.config import Config

from constants import paths, radar, colors

_logger = logging.getLogger(__name__)


def _run_and_check(cmd):
    _logger.info('command:')
    _logger.info(' '.join(cmd))
    try:
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except subprocess.CalledProcessError as e:
        _logger.error(f'Command failed with exit code {e.returncode}')
        _logger.error(f'STDOUT: {e.stdout}')
        _logger.error(f'STDERR: {e.stderr}')
        raise


def render():
    config = Config.instance()

    min_lat = config['bbox']['min_lat']
    min_lon = config['bbox']['min_lon']
    max_lat = config['bbox']['max_lat']
    max_lon = config['bbox']['max_lon']

    cmds = []
    
    # Convert raw data to GeoJSONs
    cmd = [
        paths.NEXRAD_JSON_BIN.as_posix(), 
        '--minimum', '10', 
        '-e', '1-3', 
        '-p', 'REF', 
        '-o', paths.RADAR_JSON_BASENAME.as_posix(), 
        paths.RADAR_RAW.as_posix()
    ]
    cmds.append(cmd)

    # Rasterize each elevation
    for i in range(1, 4):
        cmd = [
            'gdal_rasterize', 
            '-q', 
            '-a', 'value', 
            '-ot', 'byte', 
            '-te', str(min_lon), str(min_lat), str(max_lon), str(max_lat),
            '-ts', str(radar.WIDTH), str(radar.HEIGHT),
            f'{paths.RADAR_JSON_BASENAME.as_posix()}-REF-{i}.json',
            f'{paths.RADAR_ELEVATION_TIF_BASENAME.as_posix()}-REF-{i}.tif'
        ]
        cmds.append(cmd)

    # Composite
    cmd = [
        'gdal_calc.py', 
        f'-A'
    ] + [
        f'{paths.RADAR_ELEVATION_TIF_BASENAME.as_posix()}-REF-{i}.tif' for i in range(1, 4)
    ] + [ 
        '--overwrite',
        f'--outfile={paths.RADAR_TIF.as_posix()}', 
        '--quiet', 
        '--calc=numpy.max(A,axis=0)'
    ]
    cmds.append(cmd)

    # Colorize
    cmd = [
        'gdaldem', 
        'color-relief', 
        '-q', 
        paths.RADAR_TIF.as_posix(),
        'gdal-colors.txt', 
        '-alpha', 
        '-nearest_color_entry', 
        paths.RADAR_TIF.as_posix()
    ]
    cmds.append(cmd)

    # Convert to PNG
    cmd = [
        'gdal_translate', 
        '-q', 
        '-of', 'PNG', 
        paths.RADAR_TIF.as_posix(), 
        paths.RADAR_IMG.as_posix()
    ]
    cmds.append(cmd)

    for cmd in cmds:
        _run_and_check(cmd)

    image = Image.new('RGBA', (radar.WIDTH, radar.HEIGHT), colors.BLACK) # type: ignore
    radar_img = Image.open(paths.RADAR_IMG)
    streets = Image.open(paths.STREETS_IMG)
    image.paste(radar_img, (0, 0), radar_img)
    image.paste(streets, (0, 0), streets)
    image.save(paths.RADAR_IMG)