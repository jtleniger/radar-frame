from PIL import Image

from sources import open_meteo
from components.forecast import components

from constants import paths, frame

def render(config, data: open_meteo.Response):
    image = Image.new("RGB", (frame.WIDTH, frame.HEIGHT), "#FFF")

    current = components.current_conditions(config, data)
    image.paste(current, (0, (image.height // 2) - (current.height // 2)))
    
    y = 0
    for d in data.forecast.days:
        day = components.day(d)
        image.paste(day, (current.width, y))
        y += day.height


    # Quantize image to color palette
    palette = Image.open(paths.PALETTE_IMG)

    image = image.quantize(7, palette=palette, dither=Image.Dither.NONE)

    image.save(paths.OUTPUT_IMG)