from PIL import ImageFont
from enum import Enum, auto

def _get_font(size, double = False):
    base_size = int(size[-2:])
    
    return ImageFont.truetype(
        f'./components/font/spleen-{size}.otf',
        base_size * 2 if double else base_size)

class Size(Enum):
    Small = auto()
    Large = auto()
    XLarge = auto()


SIZES = {
    Size.Small: _get_font('16x32'),
    Size.Large: _get_font('32x64'),
    Size.XLarge: _get_font('32x64', True)
}