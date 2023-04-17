import logging
from PIL import Image, ImageDraw

from constants import colors, paths

logger = logging.getLogger(__name__)

def create():
    if paths.PALETTE_IMG.exists():
        logger.info(f'{paths.PALETTE_IMG} exists, doing nothing')

    palette_colors = [colors.BLACK, colors.WHITE, colors.RED, colors.ORANGE, colors.YELLOW, colors.GREEN, colors.BLUE]
    palette = Image.new("P", (len(palette_colors), 1))

    draw = ImageDraw.Draw(palette)

    for i, color in enumerate(palette_colors):
        draw.point((i, 0), color)

    palette.save(paths.PALETTE_IMG)