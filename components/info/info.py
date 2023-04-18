from PIL import Image, ImageDraw
from typing import List
from datetime import datetime
from pytz import timezone
from datetime import datetime, timezone as pytimezone

from components.font import font
from config.config import Config
from constants import frame, colors, info
from sources.nws_api import Alert, AlertLevel

_ALERT_COLORS = {
    AlertLevel.Info: {
        'fg': colors.WHITE,
        'bg': colors.BLACK
    },
    AlertLevel.Watch: {
        'fg': colors.BLACK,
        'bg': colors.YELLOW
    },
    AlertLevel.Warning: {
        'fg': colors.BLACK,
        'bg': colors.ORANGE
    },
    AlertLevel.Emergency: {
        'fg': colors.WHITE,
        'bg': colors.RED
    }
}


def render(alerts: List[Alert]) -> Image.Image:
    config = Config.instance()
    image = Image.new("RGBA", (frame.WIDTH, info.HEIGHT), colors.BLACK)
    draw = ImageDraw.Draw(image)

    now_utc = datetime.now(tz=pytimezone.utc)
    local_tz = timezone(config['forecast']['timezone'])
    now_local = now_utc.astimezone(local_tz)

    draw.text((image.width - 18, image.height // 2 - 2), f"updated: {now_local.strftime('%-I:%M%p')}", font=font.SIZES[font.Size.Small], fill=colors.WHITE, anchor="rm")

    if not alerts:
        return image
    
    alerts.sort(key=lambda a: a.level.value)

    most_severe = alerts[0]

    alert_colors = _ALERT_COLORS[most_severe.level]

    count = len(alerts)

    alert_text = most_severe.event

    if count > 1:
        alert_text += f' and {count - 1} others'

    draw.rectangle(((0, 0), (5 * (frame.WIDTH) // 8, info.HEIGHT)), fill=alert_colors['bg'])
    draw.text((18, image.height // 2 - 2), alert_text, font=font.SIZES[font.Size.Small], fill=alert_colors['fg'], anchor='lm')

    return image