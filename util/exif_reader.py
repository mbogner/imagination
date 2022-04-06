from datetime import datetime, timezone
from typing import Optional

import piexif
from PIL import Image, ExifTags

from logger import logger
from model.coordinates import Coordinates
from model.media_file import MediaFile
from model.media_type import MediaType
from model.ts_source import TsSource


class ExifReader:
    codec = 'utf-8'

    @staticmethod
    def enrich_with_exif_data(media_files: list[MediaFile]) -> None:
        logger.info('enriching media files from exif')
        for media_file in media_files:
            if media_file.media_type == MediaType.JPG:
                img = Image.open(media_file.original_path)
                raw = piexif.load(img.info.get('exif'))

                exif = ExifReader.exif_to_hash(raw['Exif'], ExifTags.TAGS)
                timestamp = ExifReader.get_timestamp(exif, ExifReader.codec)
                media_file.update_time(timestamp)

                gps = ExifReader.exif_to_hash(raw['GPS'], ExifTags.GPSTAGS)
                coordinates = ExifReader.get_coordinates(gps)
                media_file.update_coordinates(coordinates)

                if media_file.has_timestamp():
                    media_file.ts_source = TsSource.EXIF
                    logger.debug(f"updated {media_file} from exif")

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
    def get_timestamp(exif, codec: str = 'utf-8') -> Optional[datetime]:
        if 'DateTimeOriginal' in exif and 'OffsetTimeOriginal' in exif:
            ts = exif['DateTimeOriginal'].decode(codec)
            offset = exif['OffsetTimeOriginal'].decode(codec)
            return datetime.strptime(f'{ts}{offset}', "%Y:%m:%d %H:%M:%S%z").astimezone(tz=timezone.utc)
        return None

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
