from PIL import Image

from constants import paths, frame

def render(config):
    # Load images
    forecast = Image.open(paths.FORECAST_IMG)
    radar = Image.open(paths.RADAR_IMG)

    # Merge
    merged = Image.new("RGB", (frame.WIDTH, frame.HEIGHT))

    merged.paste(forecast)
    merged.paste(radar, (frame.WIDTH - frame.HEIGHT, 0))

    # Quantize image to color palette
    palette = Image.open(paths.PALETTE_IMG)

    merged = merged.quantize(7, palette=palette, dither=Image.Dither.NONE)

    merged.save(paths.OUTPUT_IMG)