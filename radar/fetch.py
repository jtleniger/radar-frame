import boto3
from botocore import UNSIGNED
from botocore.config import Config
from datetime import timedelta, timezone, datetime

BUCKET = 'noaa-nexrad-level2'


def date_string(date: datetime):
    return date.date().strftime('%Y/%m/%d')


def fetch_radar(config):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    nexrad_id = config['radar']['nexrad_id']
    now = datetime.now(tz=timezone.utc)

    # List objects and find latest
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=f'{date_string(now)}/{nexrad_id}')

    # If we don't have contents, we might be at the date change for UTC; try yesterday
    if 'Contents' not in response:
        yesterday = (now - timedelta(days=1))
        response = s3.list_objects_v2(Bucket=BUCKET, Prefix=f'{date_string(yesterday)}/{nexrad_id}')

    objects = response['Contents']
    objects = list(filter(lambda o: not o['Key'].endswith('_MDM'), objects))
    objects.sort(reverse=True, key=lambda o: o['LastModified'])

    latest = objects[0]

    # Download latest
    s3.download_file(BUCKET, latest['Key'], config['files']['radar_raw'])
