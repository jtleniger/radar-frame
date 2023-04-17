from PIL import Image, ImageDraw
from typing import List

from sources import open_meteo
from components.forecast import components
from constants import paths, frame


def render(current: open_meteo.CurrentConditions, hourly: List[open_meteo.ForecastHour], daily: List[open_meteo.ForecastDay]):
    image = Image.new("RGB", (frame.WIDTH, frame.HEIGHT), "#FFF")

    left_column_width = frame.WIDTH - frame.HEIGHT

    draw = ImageDraw.Draw(image)

    draw.line(((left_column_width - 32, 32), (left_column_width - 32, frame.HEIGHT - 60)), '#000', 1)

    current_img = components.current_conditions(current)
    image.paste(current_img, ((left_column_width - current_img.width) // 2 - 16, 16))

    hourly_img = components.hourly_forecast(hourly)
    image.paste(hourly_img, (42, current_img.height))
 
    daily_img = components.daily_forecast(daily)
    image.paste(daily_img, (left_column_width, 16))

    palette = Image.open(paths.PALETTE_IMG)
    image = image.quantize(7, palette=palette, dither=Image.Dither.NONE)

    image.save(paths.OUTPUT_IMG)
