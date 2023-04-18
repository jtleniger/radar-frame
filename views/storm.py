from typing import List
from PIL import Image
from components.forecast import components
from components.info import info
from constants import paths, frame
from sources import open_meteo, nws_api

def render(
        current: open_meteo.CurrentConditions,
        hourly: List[open_meteo.ForecastHour],
        alerts: List[nws_api.Alert]):
    
    image = Image.new("RGB", (frame.WIDTH, frame.HEIGHT), "#FFF")

    left_column_width = frame.WIDTH - frame.HEIGHT

    current_img = components.current_conditions(current)
    image.paste(current_img, ((left_column_width - current_img.width) // 2, 8))

    hourly_img = components.hourly_forecast(hourly)
    image.paste(hourly_img, (56, current_img.height))

    radar = Image.open(paths.RADAR_IMG)
    image.paste(radar, (frame.WIDTH - frame.HEIGHT, 0))

    info_img = info.render(alerts)
    image.paste(info_img, (0, frame.HEIGHT - info_img.height))

    palette = Image.open(paths.PALETTE_IMG)
    image = image.quantize(7, palette=palette, dither=Image.Dither.NONE)

    image.save(paths.OUTPUT_IMG)