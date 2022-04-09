import os.path
from datetime import datetime, timezone
from typing import Optional

import piexif

from model.media_file import MediaFile
from model.media_type import MediaType
from model.ts_source import TsSource

TS_FORMAT = "%Y:%m:%d %H:%M:%S"
ENCODING = 'utf-8'
UTC_TZ_BINARY = '+00:00'.encode(ENCODING)

# see PIL.ExifTags
ExifKey = 'Exif'
DateTimeOriginal = 0x9003
OffsetTimeOriginal = 0x9011


class ExifWriter:

    @staticmethod
    def translate_utc_to_exif(ts: datetime) -> Optional[dict]:
        if ts is None:
            return None
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        if ts.tzinfo != timezone.utc:
            ts = ts.astimezone(timezone.utc)
        return {
            ExifKey: {
                DateTimeOriginal: ts.strftime(TS_FORMAT).encode(ENCODING),
                OffsetTimeOriginal: UTC_TZ_BINARY,
            }
        }

    @staticmethod
    def write_exif_to_file(exif_dict: dict, file: str):
        if exif_dict is not None and file is not None and os.path.isfile(file):
            piexif.insert(piexif.dump(exif_dict), file)

    @staticmethod
    def add_exif_to_jpg_if_missing(media_files: list[MediaFile]) -> None:
        for media_file in media_files:
            if media_file.ts_source != TsSource.EXIF and media_file.media_type == MediaType.JPG \
                    and os.path.isfile(media_file.target):
                exif_dict = ExifWriter.translate_utc_to_exif(media_file.timestamp)
                piexif.insert(piexif.dump(exif_dict), media_file.target)
