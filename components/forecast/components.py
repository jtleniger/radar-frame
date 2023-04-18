from PIL import Image, ImageDraw
from typing import List
from constants import frame, colors

import components.forecast.codes as codes
import components.forecast.icon as icons
from components.font import font
from sources import open_meteo


def current_conditions(current: open_meteo.CurrentConditions) -> Image.Image:
    image = Image.new("RGBA", (256, 192), colors.WHITE)

    draw = ImageDraw.Draw(image)
    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    y = 0
    draw.text((image.width / 2 + 12, y), f"{str(round(current.temp_f))}°",
              font=font.SIZES[font.Size.Large], fill=colors.BLACK, anchor="mt")
    y += 72

    icon = codes.code_to_img(current.code, not current.is_day, 96)
    image.paste(icon, ((image.width // 2) - 48, y - 24), icon)
    y += 64

    draw.text((image.width / 2, y),
              f"{(codes.code_to_string(current.code))}", font=font.SIZES[font.Size.Small], fill=colors.BLACK, anchor="mt")

    return image


def forecast_day(day: open_meteo.ForecastDay) -> Image.Image:
    image = Image.new("RGBA", (frame.HEIGHT, 60), colors.WHITE)
    draw = ImageDraw.Draw(image)

    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    x = 0

    # Day
    draw.text((x, 8), f"{day.day}", font=font.SIZES[font.Size.Small], fill=colors.BLACK)

    x += 128

    # Icon
    icon = codes.code_to_img(day.code, False, 48)
    image.paste(icon, (x, 0), icon)

    x += 128

    # High & Low
    draw.text((x, 8),
              f"{str(round(day.high_f)) + '°':>4} / {str(round(day.low_f)) + '°':>4}", font=font.SIZES[font.Size.Small], fill=colors.BLACK)

    return image


def daily_forecast(days: List[open_meteo.ForecastDay]) -> Image.Image:
    image = Image.new("RGBA", (frame.HEIGHT, 60 * len(days)), colors.WHITE)

    y = 0
    for d in days:
        day = forecast_day(d)
        image.paste(day, (0, y))
        y += day.height

    return image


def forecast_hour(hour: open_meteo.ForecastHour) -> Image.Image:
    image = Image.new("RGBA", (220, 48), colors.WHITE)

    draw = ImageDraw.Draw(image)

    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    x = 0

    draw.text((x, 0), hour.hour, font=font.SIZES[font.Size.Small], fill=colors.BLACK)

    x += 84

    icon = codes.code_to_img(hour.code, False, 40)
    image.paste(icon, (x, 0), icon)

    x += 60

    draw.text((x, 0), f"{str(round(hour.temp_f)) + '°':>4}", font=font.SIZES[font.Size.Small], fill=colors.BLACK)

    return image


def hourly_forecast(hours: List[open_meteo.ForecastHour]) -> Image.Image:
    image = Image.new("RGBA", (220, 48 * len(hours)), colors.WHITE)

    y = 0
    for h in hours:
        hour = forecast_hour(h)
        image.paste(hour, (0, y))
        y += hour.height

    return image
