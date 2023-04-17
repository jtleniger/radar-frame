from PIL import Image, ImageDraw, ImageFont
from typing import List
from constants import frame

import components.forecast.codes as codes
import components.forecast.icon as icons
from sources import open_meteo

_WHITE = '#FFF'
_BLACK = '#000'


def _get_font(size):
    return ImageFont.truetype("terminess.ttf", size)


_FONTS = {
    'xsmall': _get_font(round(22)),
    'small': _get_font(round(32)),
    'medium': _get_font(round(48)),
    'large': _get_font(round(64))
}


def current_conditions(current: open_meteo.CurrentConditions) -> Image.Image:
    image = Image.new("RGBA", (190, 200), _WHITE)

    draw = ImageDraw.Draw(image)
    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    y = 0
    draw.text((image.width / 2 + 12, y), f"{str(round(current.temp_f))}°",
              font=_FONTS['large'], fill=_BLACK, anchor="mt")
    y += 72

    icon = codes.code_to_img(current.code, not current.is_day, 96)
    image.paste(icon, ((image.width // 2) - 48, y - 24), icon)
    y += 64

    draw.text((image.width / 2, y),
              f"{(codes.code_to_string(current.code))}", font=_FONTS['small'], fill=_BLACK, anchor="mt")

    return image


def forecast_day(day: open_meteo.ForecastDay) -> Image.Image:
    image = Image.new("RGBA", (frame.HEIGHT, 60), _WHITE)
    draw = ImageDraw.Draw(image)

    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    x = 0

    # Day
    draw.text((x, 8), f"{day.day}", font=_FONTS['small'], fill=_BLACK)

    x += 72

    # Icon
    icon = codes.code_to_img(day.code, False, 48)
    image.paste(icon, (x, 8), icon)

    x += 64

    # High & Low
    draw.text((x, 8),
              f"{str(round(day.high_f)) + '°':>4} / {str(round(day.low_f)) + '°':>4}", font=_FONTS['small'], fill=_BLACK)

    x += 192

    # Wind
    icon = icons.get_icon_as_png('wi-strong-wind', 32)
    image.paste(icon, (x, 0), icon)

    draw.text((x + 32, 0), f"{str(round(day.wind_mph)):>3}" + "mph", font=_FONTS['xsmall'], fill=_BLACK)

    # Rain
    icon = icons.get_icon_as_png('wi-raindrop', 32)
    image.paste(icon, (x, 24), icon)

    draw.text((x + 48, 24), f"{str(round(day.precip_sum, 1)):>4}" + '"', font=_FONTS['xsmall'], fill=_BLACK)

    return image


def daily_forecast(days: List[open_meteo.ForecastDay]) -> Image.Image:
    image = Image.new("RGBA", (frame.HEIGHT, 60 * len(days)), _WHITE)

    y = 0
    for d in days:
        day = forecast_day(d)
        image.paste(day, (0, y))
        y += day.height

    return image


def forecast_hour(hour: open_meteo.ForecastHour) -> Image.Image:
    image = Image.new("RGBA", (220, 48), _WHITE)

    draw = ImageDraw.Draw(image)

    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    x = 0

    draw.text((x, 0), hour.hour, font=_FONTS['small'], fill=_BLACK)

    x += 84

    icon = codes.code_to_img(hour.code, False, 40)
    image.paste(icon, (x, 0), icon)

    x += 60

    draw.text((x, 0), f"{str(round(hour.temp_f)) + '°':>4}", font=_FONTS['small'], fill=_BLACK)

    return image


def hourly_forecast(hours: List[open_meteo.ForecastHour]) -> Image.Image:
    image = Image.new("RGBA", (220, 48 * len(hours)), _WHITE)

    y = 0
    for h in hours:
        hour = forecast_hour(h)
        image.paste(hour, (0, y))
        y += hour.height

    return image
