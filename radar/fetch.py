import logging
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from datetime import timedelta, timezone, datetime
from dataclasses import dataclass

BUCKET = 'noaa-nexrad-level2'

logger = logging.getLogger(__name__)


@dataclass
class LatestObject:
    key: str
    last_modified: datetime


def date_string(date: datetime):
    return date.date().strftime('%Y/%m/%d')


def latest_object(config):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    nexrad_id = config['radar']['nexrad_id']
    now = datetime.now(tz=timezone.utc)

    prefix = f'{date_string(now)}/{nexrad_id}'

    # List objects and find latest
    response = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)

    # If there are no results, we might be at the date change for UTC; try yesterday
    if 'Contents' not in response:
        yesterday = (now - timedelta(days=1))
        prefix = f'{date_string(yesterday)}/{nexrad_id}'
        response = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)

    if not 'Contents':
        logger.error(f'no "Contents" key in s3 response for prefix {prefix}')
        return None

    objects = response['Contents']
    objects = list(filter(lambda o: not o['Key'].endswith('_MDM'), objects))

    if not objects:
        logger.error(f'no objects found for prefix {prefix}')
        return None

    objects.sort(reverse=True, key=lambda o: o['LastModified'])

    latest = objects[0]

    return LatestObject(key=latest['Key'], last_modified=latest['LastModified'])


def fetch_radar(config, obj: LatestObject):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    # Download latest
    s3.download_file(BUCKET, obj.key, config['files']['radar_raw'])
