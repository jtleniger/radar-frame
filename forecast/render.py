from PIL import Image, ImageDraw, ImageFont
import forecast.codes as codes
import forecast.icon as icons

from forecast.current import CurrentConditions
from forecast.day import Day

BLACK = '#000'
WIDTH = 800 - 480


def get_font(size):
    return ImageFont.truetype("terminess.ttf", size)


def create_weather_image(current: CurrentConditions, forecast: list[Day]):
    # Set up image
    image = Image.new("RGBA", (WIDTH, 480), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.fontmode = '1'  # type: ignore

    # Set up fonts
    fonts = {
        'xsmall': get_font(14),
        'small': get_font(32),
        'medium': get_font(48),
        'large': get_font(64)
    }

    # Draw current conditions
    y = 16
    draw.text((WIDTH / 2 + 12, y), f"{str(round(current.temp_f))}°", font=fonts['large'], fill=BLACK, anchor="mt")
    y += 72

    icon = codes.code_to_img(current.code, False, 96)
    image.paste(icon, ((WIDTH // 2) - 48, y - 24), icon)
    y += 64

    draw.text((WIDTH / 2, y),
              f"{(codes.code_to_string(current.code))}", font=fonts['small'], fill=BLACK, anchor="mt")

    # Draw 5-day forecast
    y += 52
    for day in forecast[:5]:
        x = 24

        draw.line([(36, y - 10), (WIDTH - 36, y - 10)], fill=BLACK, width=1)

        # Day
        draw.text((x, y + 12), f"{day.day}", font=fonts['xsmall'], fill=BLACK)
        x += 72

        # Icon
        icon = codes.code_to_img(day.code, False, 32)
        image.paste(icon, (x, y - 8), icon)
        x += 32

        # High & Low
        draw.text((x, y),
                  f"{str(round(day.high_f)) + '°':>5} / {str(round(day.low_f)) + '°':>5}", font=fonts['xsmall'], fill=BLACK)
        x += 88

        y += 24
        x = 96

        # Wind
        icon = icons.get_icon_as_png('wi-strong-wind', 24)
        image.paste(icon, (x, y - 2), icon)
        x += 26

        draw.text((x, y), f"{str(round(day.wind)) + ' mph':>7}", font=fonts['xsmall'], fill=BLACK)
        x += 48

        # Rain
        icon = icons.get_icon_as_png('wi-raindrop', 24)
        image.paste(icon, (x, y - 2), icon)
        x += 20

        draw.text((x, y), f"{str(round(day.precip_sum, 1)) + ' in':>7}", font=fonts['xsmall'], fill=BLACK)
        

        y += 32

    # Draw line on RHS
    line_width = 2
    line_x = image.width - line_width
    draw.line([(line_x, 0), (line_x, image.height)], fill='#000', width=line_width)

    # Save image
    image.save("forecast.png")
