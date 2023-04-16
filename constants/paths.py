import os
from pathlib import Path

DATA_DIR = Path(os.getcwd()) / 'data'
STREETS_DATA = DATA_DIR / 'streets.osm'
STREETS_TIF = DATA_DIR / 'streets.tif'
STREETS_IMG = DATA_DIR / 'streets.png'
RADAR_RAW = DATA_DIR / 'nexrad-latest-raw'
PALETTE_IMG = DATA_DIR / 'palette.png'
FORECAST_IMG = DATA_DIR / 'forecast.png'
RADAR_IMG = DATA_DIR / 'radar.png'
OUTPUT_IMG = DATA_DIR / 'frame.png'