from PIL import Image

def create(config):
    frame_config = config['frame']
    palette_config = config['radar.palette']
    file_config = config['files']

    width = int(frame_config['width'])
    height = int(frame_config['height'])

    # Load images
    forecast = Image.open(file_config['forecast_img'])
    radar = Image.open(file_config['radar_img'])

    # # Crop radar to square
    # dimension = radar.width if radar.width < radar.height else radar.height

    # radar = radar.crop((0, 0, dimension, dimension))

    # # Resize radar to fit height
    # radar = radar.resize((height, height), resample=Image.NEAREST)

    merged = Image.new("RGB", (width, height))

    merged.paste(forecast)
    merged.paste(radar, (width - height, 0))

    # Squash image to color palette
    palette = Image.open(file_config['palette_img'])

    merged = merged.quantize(len(palette_config['colors']), palette=palette, dither=Image.Dither.NONE)

    merged.save(file_config['output_img'])