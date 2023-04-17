from PIL import ImageFont
from enum import Enum, auto

def _get_font(size):
    return ImageFont.truetype("./components/font/terminess.ttf", size)

class Size(Enum):
    XSmall = auto()
    Small = auto()
    Medium = auto()
    Large = auto()


SIZES = {
    Size.XSmall: _get_font(22),
    Size.Small: _get_font(32),
    Size.Medium: _get_font(48),
    Size.Large: _get_font(64)
}