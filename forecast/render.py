from PIL import Image, ImageDraw, ImageFont
import forecast.codes as codes
import forecast.icon as icons

from forecast.current import CurrentConditions
from forecast.day import Day
from pytz import timezone
from datetime import datetime, timezone as pytimezone

WHITE = '#FFF'
BLACK = '#000'


def get_font(size):
    return ImageFont.truetype("terminess.ttf", size)


def render_image(config, current: CurrentConditions, forecast: list[Day]):
    frame_config = config['frame']
    file_config = config['files']

    height = int(frame_config['height'])
    scale = height / 480
    width = int(frame_config['width']) - height

    large_icon_size = round(96 * scale)
    medium_icon_size = round(32 * scale)
    small_icon_size = round(24 * scale)

    # Set up image
    image = Image.new("RGBA", (width, height), WHITE)
    draw = ImageDraw.Draw(image)

    # Disables antialiasing
    draw.fontmode = '1'  # type: ignore

    # Set up fonts
    fonts = {
        'xsmall': get_font(round(14 * scale)),
        'small': get_font(round(32 * scale)),
        'medium': get_font(round(48 * scale)),
        'large': get_font(round(64 * scale))
    }

    # Draw current conditions
    y = 16
    draw.text((width / 2 + 12, y), f"{str(round(current.temp_f))}°", font=fonts['large'], fill=BLACK, anchor="mt")
    y += round(72 * scale)

    now_utc = datetime.now(tz=pytimezone.utc)
    local_tz = timezone(config['forecast']['timezone'])
    now_local = now_utc.astimezone(local_tz)

    icon = codes.code_to_img(current.code, current.is_night(now_local), large_icon_size)
    image.paste(icon, ((width // 2) - round(48 * scale), y - round(24 * scale)), icon)
    y += round(64 * scale)

    draw.text((width / 2, y),
              f"{(codes.code_to_string(current.code))}", font=fonts['small'], fill=BLACK, anchor="mt")

    # Draw 5-day forecast
    y += round(52 * scale)
    for day in forecast[:5]:
        x = 24

        draw.line([(36, y - round(10 * scale)), (width - 36, y - round(10 * scale))], fill=BLACK, width=1)

        # Day
        draw.text((x, y + round(12 * scale)), f"{day.day}", font=fonts['xsmall'], fill=BLACK)
        x += round(72 * scale)

        # Icon
        icon = codes.code_to_img(day.code, False, medium_icon_size)
        image.paste(icon, (x, y - round(8 * scale)), icon)
        x += round(32 * scale)

        # High & Low
        draw.text((x, y),
                  f"{str(round(day.high_f)) + '°':>5} / {str(round(day.low_f)) + '°':>5}", font=fonts['xsmall'], fill=BLACK)

        y += round(24 * scale)
        x = round(96 * scale)

        # Wind
        icon = icons.get_icon_as_png('wi-strong-wind', small_icon_size)
        image.paste(icon, (x, y - round(2 * scale)), icon)
        x += round(26 * scale)

        draw.text((x, y), f"{str(round(day.wind)) + ' mph':>7}", font=fonts['xsmall'], fill=BLACK)
        x += round(48 * scale)

        # Rain
        icon = icons.get_icon_as_png('wi-raindrop', small_icon_size)
        image.paste(icon, (x, y - round(2 * scale)), icon)
        x += round(20 * scale)

        draw.text((x, y), f"{str(round(day.precip_sum, 1)) + ' in':>7}", font=fonts['xsmall'], fill=BLACK)
        

        y += round(32 * scale)

    # Draw line on RHS
    line_width = 2
    line_x = image.width - line_width
    draw.line([(line_x, 0), (line_x, image.height)], fill=BLACK, width=line_width)

    # Save image
    image.save(file_config['forecast_img'])
