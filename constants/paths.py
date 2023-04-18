import os
from pathlib import Path

DATA_DIR = Path(os.getcwd()) / 'data'

STREETS_DATA = DATA_DIR / 'streets.osm'
STREETS_TIF = DATA_DIR / 'streets.tif'
STREETS_IMG = DATA_DIR / 'streets.png'

PALETTE_IMG = DATA_DIR / 'palette.png'

RADAR_IMG = DATA_DIR / 'nexrad-latest.png'
RADAR_RAW = DATA_DIR / 'nexrad-latest.ar2'
RADAR_CSV = DATA_DIR / 'nexrad-latest.csv'
RADAR_SHP = DATA_DIR / 'nexrad-latest.shp'
RADAR_TIF = DATA_DIR / 'nexrad-latest.tif'

OUTPUT_IMG = DATA_DIR / 'frame.png'


BIN_DIR = Path(os.getcwd()) / 'bin'

NEXRAD_CSV_BIN = BIN_DIR / 'nexrad-csv-amd64'