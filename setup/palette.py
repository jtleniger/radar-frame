from PIL import Image, ImageDraw

def create(config):
    colors = config['radar.palette']['colors'].split(',')

    palette = Image.new("P", (len(colors), 1))

    draw = ImageDraw.Draw(palette)

    for i, color in enumerate(colors):
        draw.point((i, 0), color)

    palette.save(config['files']['palette_img'])