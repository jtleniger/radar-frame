from PIL import Image

def render(config):
    frame_config = config['frame']
    palette_config = config['radar.palette']
    file_config = config['files']

    width = int(frame_config['width'])
    height = int(frame_config['height'])

    # Load images
    forecast = Image.open(file_config['forecast_img'])
    radar = Image.open(file_config['radar_img'])

    # Merge
    merged = Image.new("RGB", (width, height))

    merged.paste(forecast)
    merged.paste(radar, (width - height, 0))

    # Quantize image to color palette
    palette = Image.open(file_config['palette_img'])

    merged = merged.quantize(len(palette_config['colors']), palette=palette, dither=Image.Dither.NONE)

    merged.save(file_config['output_img'])