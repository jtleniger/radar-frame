from typing import List
from PIL import Image
from components.forecast import components

from constants import paths, frame
from sources import open_meteo

def render(current: open_meteo.CurrentConditions, hourly: List[open_meteo.ForecastHour]):
    image = Image.new("RGB", (frame.WIDTH, frame.HEIGHT), "#FFF")

    left_column_width = frame.WIDTH - frame.HEIGHT

    current_img = components.current_conditions(current)
    image.paste(current_img, ((left_column_width - current_img.width) // 2, 16))

    hourly_img = components.hourly_forecast(hourly)
    image.paste(hourly_img, (56, current_img.height))

    radar = Image.open(paths.RADAR_IMG)

    image.paste(radar, (frame.WIDTH - frame.HEIGHT, 0))

    palette = Image.open(paths.PALETTE_IMG)
    image = image.quantize(7, palette=palette, dither=Image.Dither.NONE)

    image.save(paths.OUTPUT_IMG)