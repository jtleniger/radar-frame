from PIL import Image, ImageDraw, ImageFont
import components.forecast.codes as codes
import components.forecast.icon as icons

from sources import open_meteo
from pytz import timezone
from datetime import datetime, timezone as pytimezone

from constants import paths, frame

_WHITE = '#FFF'
_BLACK = '#000'


def get_font(size):
    return ImageFont.truetype("terminess.ttf", size)

_FONTS =  {
    'xsmall': get_font(round(14)),
    'small': get_font(round(32)),
    'medium': get_font(round(48)),
    'large': get_font(round(64))
}


def current_conditions(config, res: open_meteo.Response):
    image = Image.new("RGBA", (190, 190), _WHITE)

    draw = ImageDraw.Draw(image)
    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    y = 16
    draw.text((image.width / 2 + 12, y), f"{str(round(res.current_conditions.temp_f))}°",
              font=_FONTS['large'], fill=_BLACK, anchor="mt")
    y += round(72)

    now_utc = datetime.now(tz=pytimezone.utc)
    local_tz = timezone(config['forecast']['timezone'])
    now_local = now_utc.astimezone(local_tz)

    icon = codes.code_to_img(res.current_conditions.code, res.current_conditions.is_night(now_local), 96)
    image.paste(icon, ((image.width // 2) - 48, y - 24), icon)
    y += 64

    draw.text((image.width / 2, y),
              f"{(codes.code_to_string(res.current_conditions.code))}", font=_FONTS['small'], fill=_BLACK, anchor="mt")
    
    return image

def day(day: open_meteo.ForecastDay):
    image = Image.new("RGBA", (320, 56), _WHITE)
    draw = ImageDraw.Draw(image)

    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    y = 0

    draw.line([36, y, (image.width - 36, y)], fill=_BLACK, width=1)

    y += 12

    x = 96

    # Icon
    icon = codes.code_to_img(day.code, False, 32)
    image.paste(icon, (x, y - 8), icon)

    x += 26

    # High & Low
    draw.text((x, y),
                f"{str(round(day.high_f)) + '°':>5} / {str(round(day.low_f)) + '°':>5}", font=_FONTS['xsmall'], fill=_BLACK)

    y += 12
    x = 24

    # Day
    draw.text((x, y), f"{day.day}", font=_FONTS['xsmall'], fill=_BLACK)

    y += 12
    x = 96

    # Wind
    icon = icons.get_icon_as_png('wi-strong-wind', 24)
    image.paste(icon, (x, y - 2), icon)
    x += 26

    draw.text((x, y), f"{str(round(day.wind)) + ' mph':>7}", font=_FONTS['xsmall'], fill=_BLACK)
    x += 54

    # Rain
    icon = icons.get_icon_as_png('wi-raindrop', 24)
    image.paste(icon, (x, y - 2), icon)
    x += 20

    draw.text((x, y), f"{str(round(day.precip_sum, 1)) + ' in':>7}", font=_FONTS['xsmall'], fill=_BLACK)

    return image
