from typing import List
from PIL import Image

from components.info import info
from constants import paths, frame
from sources import forecast

def render(alerts: List[forecast.Alert]):
    
    image = Image.new("RGB", (frame.WIDTH, frame.HEIGHT), "#FFF") # type: ignore

    radar = Image.open(paths.RADAR_IMG)
    image.paste(radar, (0, 0))

    info_img = info.render(alerts)
    image.paste(info_img, (0, frame.HEIGHT - info_img.height))

    palette = Image.open(paths.PALETTE_IMG)
    image = image.quantize(7, palette=palette)

    image.save(paths.OUTPUT_IMG)