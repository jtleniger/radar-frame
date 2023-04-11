import logging
import boto3
from botocore import UNSIGNED
from botocore.config import Config
from datetime import timedelta, timezone, datetime
from dataclasses import dataclass
from typing import Optional

_BUCKET = 'noaa-nexrad-level2'

_logger = logging.getLogger(__name__)


@dataclass
class Object:
    key: str
    last_modified: datetime


def _key_date_string(date: datetime) -> str:
    return date.date().strftime('%Y/%m/%d')


def latest_object(nexrad_id: str) -> Optional[Object]:
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    nexrad_id = nexrad_id
    now = datetime.now(tz=timezone.utc)

    prefix = f'{_key_date_string(now)}/{nexrad_id}'

    response = s3.list_objects_v2(Bucket=_BUCKET, Prefix=prefix)

    # If there are no results, we might be at the date change for UTC; try yesterday
    if 'Contents' not in response:
        yesterday = (now - timedelta(days=1))
        prefix = f'{_key_date_string(yesterday)}/{nexrad_id}'
        response = s3.list_objects_v2(Bucket=_BUCKET, Prefix=prefix)

    if not 'Contents':
        _logger.error(f'no "Contents" key in s3 response for prefix {prefix}')
        return None

    objects = response['Contents']
    objects = list(filter(lambda o: not o['Key'].endswith('_MDM'), objects))

    if not objects:
        _logger.error(f'no objects found for prefix {prefix}')
        return None

    objects.sort(reverse=True, key=lambda o: o['LastModified'])

    latest = objects[0]

    return Object(key=latest['Key'], last_modified=latest['LastModified'])


def download(obj: Object, to: str) -> None:
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))
    s3.download_file(_BUCKET, obj.key, to)
