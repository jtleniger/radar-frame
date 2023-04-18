from PIL import ImageFont
from enum import Enum, auto

def _get_font(size):
    return ImageFont.truetype(f'./components/font/spleen-{size}.otf', int(size[-2:]))

class Size(Enum):
    Small = auto()
    Large = auto()


SIZES = {
    Size.Small: _get_font('16x32'),
    Size.Large: _get_font('32x64')
}