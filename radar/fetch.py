import boto3
from botocore import UNSIGNED
from botocore.config import Config
from datetime import timezone, datetime

BUCKET='noaa-nexrad-level2'

def fetch_radar(config):
    nexrad_id = config['radar']['nexrad_id']
    now = datetime.now(tz=timezone.utc)
    datestring = now.date().strftime('%Y/%m/%d')

    # List objects and find latest
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=f'{datestring}/{nexrad_id}')

    objects = response['Contents']
    objects.sort(reverse=True, key=lambda o: o['LastModified'])

    latest = objects[0]

    # Download latest
    s3.download_file(BUCKET, latest['Key'], config['files']['radar_raw'])