import logging
from PIL import Image, ImageDraw

from constants import paths

logger = logging.getLogger(__name__)

def create():
    if paths.PALETTE_IMG.exists():
        logger.info(f'{paths.PALETTE_IMG} exists, doing nothing')

    colors = ['#000','#FFF','#F00','#0F0','#00F','#FF8000','#FF0']
    palette = Image.new("P", (len(colors), 1))

    draw = ImageDraw.Draw(palette)

    for i, color in enumerate(colors):
        draw.point((i, 0), color)

    palette.save(paths.PALETTE_IMG)