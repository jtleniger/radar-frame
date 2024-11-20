from PIL import Image, ImageDraw
from typing import List
from constants import frame, colors

import components.forecast.codes as codes
from components.font import font
from sources import forecast

def debug_edges(draw, image, color):
    draw.point((0, 0), color)
    draw.point((0, image.height - 1), color)
    draw.point((image.width - 1, 0), color)
    draw.point((image.width - 1, image.height - 1), color)


def current_conditions(current: forecast.CurrentConditions) -> Image.Image:
    image = Image.new("RGBA", (frame.WIDTH_1_3, frame.HEIGHT_LESS_INFO), colors.WHITE) # type: ignore

    draw = ImageDraw.Draw(image)
    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    debug_edges(draw, image, '#F00')

    y = 40
    draw.text((image.width / 2 + 6, y), f"{str(round(current.temp_f))}",
              font=font.SIZES[font.Size.XLarge], fill=colors.BLACK, anchor="mt")
    y += frame.HEIGHT_LESS_INFO_1_3

    icon = codes.code_to_img(current.code, not current.is_day, 172)
    image.paste(icon, ((image.width // 2) - (icon.width // 2), y - 36), icon)

    y += frame.HEIGHT_LESS_INFO_1_3 + 24

    draw.text((image.width / 2 + 6, y),
              codes.code_to_string(current.code).replace(' ', '\n'),
              font=font.SIZES[font.Size.Large],
              fill=colors.BLACK,
              anchor='mt')

    return image


def forecast_day(day: forecast.ForecastDay) -> Image.Image:
    image = Image.new("RGBA", (frame.WIDTH_1_3, frame.HEIGHT_LESS_INFO // 3), colors.WHITE) # type: ignore
    draw = ImageDraw.Draw(image)

    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    y = 0
    x = 16

    # Day
    draw.text((x, y), f"{day.day}", font=font.SIZES[font.Size.Large], fill=colors.BLACK)

    x += 148

    # Icon
    icon = codes.code_to_img(day.code, False, 86)
    image.paste(icon, (x, y - 6), icon)

    x = 16
    y += 64

    # High & Low
    draw.text((x, y),
              f"{str(round(day.high_f)):<3} {str(round(day.low_f)):>3}",
              font=font.SIZES[font.Size.Large],
              fill=colors.BLACK)

    return image


def daily_forecast(days: List[forecast.ForecastDay]) -> Image.Image:
    image = Image.new("RGBA", (frame.WIDTH_1_3, frame.HEIGHT_LESS_INFO), colors.WHITE) # type: ignore

    draw = ImageDraw.Draw(image)

    y = 12
    for d in days[:3]:
        day = forecast_day(d)
        image.paste(day, (0, y))
        y += day.height

    debug_edges(draw, image, '#00F')

    return image


def forecast_hour(hour: forecast.ForecastHour) -> Image.Image:
    image = Image.new("RGBA", (frame.WIDTH_1_3, frame.HEIGHT_LESS_INFO // 3), colors.WHITE) # type: ignore

    draw = ImageDraw.Draw(image)

    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    y = 12
    x = 16

    draw.text((x, y), f"{hour.hour}", font=font.SIZES[font.Size.Large], fill=colors.BLACK)

    x += 148

    # Icon
    icon = codes.code_to_img(hour.code, False, 86)
    image.paste(icon, (x, y - 6), icon)

    x = 16
    y += 64

    draw.text((x, y),
              f"{str(round(hour.temp_f))}",
              font=font.SIZES[font.Size.Large],
              fill=colors.BLACK)

    return image


def hourly_forecast(all_hours: List[forecast.ForecastHour]) -> Image.Image:
    image = Image.new("RGBA", (frame.WIDTH_1_3, frame.HEIGHT_LESS_INFO), colors.WHITE) # type: ignore

    draw = ImageDraw.Draw(image)

    hours = [all_hours[i] for i in range(len(all_hours)) if i % 2 == 0][:3]

    y = 0
    for h in hours:
        hour = forecast_hour(h)
        image.paste(hour, (0, y))
        y += hour.height

    debug_edges(draw, image, '#0F0')

    return image
