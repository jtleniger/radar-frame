import math
import os
import platform
from PIL import Image

def render(config, dry_run):
    p = platform.platform()

    if 'x86_64' in p:
        binary = './bin/nexrad-render-amd64'
    elif 'armv7' in p:
        binary = './bin/nexrad-render-arm'
    else:
        raise Exception('unsupported platform')
    
    data_path = config['files']['radar_raw_test'] if dry_run else config['files']['radar_raw']

    cmd = f"{binary} -c scope -s 4096 -o {config['files']['radar_img']} {data_path}"

    exit_code = os.system(cmd)

    if exit_code != 0:
        raise Exception(f'{cmd} exited {exit_code}')

    center_x = 1850
    center_y = 2000
    
    radar = Image.open(config['files']['radar_img'])

    radar = radar.crop((center_x - 240, center_y - 240, center_x + 240, center_y + 240))
    radar.save(config['files']['radar_img'])