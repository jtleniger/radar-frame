from PIL import Image, ImageDraw
from typing import List

from sources import forecast
from components.forecast import components
from components.info import info
from constants import paths, frame, colors


def render(
        current: forecast.CurrentConditions,
        hourly: List[forecast.ForecastHour],
        daily: List[forecast.ForecastDay],
        alerts: List[forecast.Alert]):
    
    image = Image.new("RGB", (frame.WIDTH, frame.HEIGHT), "#FFF") # type: ignore

    draw = ImageDraw.Draw(image)

    current_img = components.current_conditions(current)
    image.paste(current_img, (0, 0))

    hourly_img = components.hourly_forecast(hourly)
    image.paste(hourly_img, (frame.WIDTH_1_3, 0))
 
    daily_img = components.daily_forecast(daily)
    image.paste(daily_img, (2 * frame.WIDTH_1_3, 0))

    info_img = info.render(alerts)
    image.paste(info_img, (0, frame.HEIGHT_LESS_INFO))

    draw.line(
        ((frame.WIDTH_1_3, 20), (frame.WIDTH_1_3, frame.HEIGHT_LESS_INFO - 20)),
        colors.BLACK, 2)
    
    draw.line(
        ((2 * frame.WIDTH_1_3, 20), (2 * frame.WIDTH_1_3, frame.HEIGHT_LESS_INFO - 20)),
        colors.BLACK, 2)

    palette = Image.open(paths.PALETTE_IMG)
    image = image.quantize(7, palette=palette, dither=Image.Dither.NONE)

    image.save(paths.OUTPUT_IMG)
