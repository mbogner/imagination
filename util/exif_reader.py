from datetime import datetime
from typing import Optional

import piexif
import pyheif
from PIL import Image, ExifTags

from logger import logger
from model.coordinates import Coordinates
from model.media_file import MediaFile
from model.media_type import MediaType
from model.ts_source import TsSource
from util.date_time_util import DateTimeUtil


class ExifReader:
    codec = 'utf-8'

    @staticmethod
    def load(media_file: MediaFile) -> Optional[dict]:
        if media_file.media_type == MediaType.JPG:
            img = Image.open(media_file.original_path)
            raw_exif = img.info.get('exif')
            if raw_exif is None:
                return None
            return piexif.load(raw_exif)
        elif media_file.media_type == MediaType.ARW:
            raw = piexif.load(media_file.original_path)
            if 'Exif' not in raw:
                return None
            return raw
        elif media_file.media_type == MediaType.HEIC:
            with open(media_file.original_path, 'rb') as file:
                heif = pyheif.read(file)
                if heif is None or heif.metadata is None:
                    return None
                for metadata in heif.metadata:
                    if 'type' not in metadata or 'Exif' != metadata['type'] or 'data' not in metadata:
                        continue
                    return piexif.load(metadata['data'])
            return None
        else:
            return None

    @staticmethod
    def enrich_with_exif_data(media_files: list[MediaFile]) -> None:
        logger.info('enriching files from exif')
        for media_file in media_files:

            if media_file.media_type == MediaType.JPG \
                    or media_file.media_type == MediaType.ARW \
                    or media_file.media_type == MediaType.HEIC:

                raw = ExifReader.load(media_file)
                if raw is None or 'Exif' not in raw:
                    continue

                exif = ExifReader.exif_to_hash(raw['Exif'], ExifTags.TAGS)
                timestamp = ExifReader.get_timestamp_from_exif(exif, ExifReader.codec)

                # alternative for getting timestamp
                if timestamp is None and '0th' in raw:
                    zeroth = ExifReader.exif_to_hash(raw['0th'], ExifTags.TAGS)
                    timestamp = ExifReader.get_timestamp_from_0th(zeroth, ExifReader.codec)

                media_file.update_time(timestamp, TsSource.EXIF, True)

                gps = ExifReader.exif_to_hash(raw['GPS'], ExifTags.GPSTAGS)
                coordinates = ExifReader.get_coordinates(gps)
                media_file.update_coordinates(coordinates)
        logger.info('enriching files from exif done')

    @staticmethod
    def exif_to_hash(data, tags) -> dict[str, str]:
        if data is None:
            return {}
        response = {}
        for key, val in data.items():
            if key in tags:
                response[tags[key]] = val
        return response

    @staticmethod
    def get_timestamp_from_exif(exif, codec: str = 'utf-8') -> Optional[datetime]:
        if 'DateTimeOriginal' in exif:
            ts: str = exif['DateTimeOriginal'].decode(codec)
            if ts.startswith('0000'):
                return None
            ts = ExifReader.fix_timestamp_str(ts)

            if 'OffsetTimeOriginal' in exif:
                offset = exif['OffsetTimeOriginal'].decode(codec)
                return datetime.strptime(f'{ts}{offset}', "%Y:%m:%d %H:%M:%S%z")

            parsed = datetime.strptime(f'{ts}', "%Y:%m:%d %H:%M:%S")
            DateTimeUtil.timezone_datetime(parsed)
            return parsed
        return None

    @staticmethod
    def get_timestamp_from_0th(zeroth, codec: str = 'utf-8') -> Optional[datetime]:
        if 'DateTime' in zeroth:
            ts: str = zeroth['DateTime'].decode(codec)
            ts = ExifReader.fix_timestamp_str(ts)
            if ts.startswith('0000'):
                return None
            return DateTimeUtil.timezone_datetime(datetime.strptime(f'{ts}', "%Y:%m:%d %H:%M:%S"))
        return None

    @staticmethod
    def fix_timestamp_str(ts: str) -> str:
        return ts.replace(" at ", " ").replace(".", ":").replace(" 24:", " 00:")

    @staticmethod
    def change_to_decimal(fraction: tuple[int, int]) -> Optional[float]:
        """convert fraction tuple to decimal
        keyword arguments: fraction -- tuple like (numerator, denominator)
        return: float"""
        return fraction[0] / fraction[1]

    @staticmethod
    def get_altitude(gps) -> Optional[float]:
        if 'GPSAltitude' in gps and 'GPSAltitudeRef' in gps:
            altitude = ExifReader.change_to_decimal(gps['GPSAltitude'])
            ref = gps['GPSAltitudeRef']
            return round(altitude + ref, 3)
        return None

    @staticmethod
    def get_coordinates(gps) -> Optional[Coordinates]:
        if 'GPSLatitude' in gps and 'GPSLatitudeRef' in gps and 'GPSLongitude' in gps and 'GPSLongitudeRef' in gps:
            lat = ExifReader.get_decimal_from_dms(gps['GPSLatitude'], gps['GPSLatitudeRef'])
            lon = ExifReader.get_decimal_from_dms(gps['GPSLongitude'], gps['GPSLongitudeRef'])
            alt = ExifReader.get_altitude(gps)
            return Coordinates(lat, lon, alt)
        return None

    @staticmethod
    def get_decimal_from_dms(dms, ref):
        if dms is None or ref is None:
            return None

        degrees = dms[0][0] / dms[0][1]
        minutes = dms[1][0] / dms[1][1] / 60.0
        seconds = dms[2][0] / dms[2][1] / 3600.0

        if ref in ['S', 'W']:
            degrees = -degrees
            minutes = -minutes
            seconds = -seconds

        return round(degrees + minutes + seconds, 8)
