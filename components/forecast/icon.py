from io import BytesIO
import cairosvg
from PIL import Image


def get_icon_as_png(icon_name, size):
    out = BytesIO()
    cairosvg.svg2png(url=f'./forecast/icons/{icon_name}.svg', write_to=out, output_height=size, output_width=size)
    image = Image.open(out)
    image = image.quantize(2)
    image = image.convert(mode='RGBA')
    return image
