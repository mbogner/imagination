import zoneinfo
from datetime import datetime

from logger import logger
from model.media_file import MediaFile
from model.ts_source import TsSource


class EvalPattern01:
    TZ = zoneinfo.ZoneInfo('Europe/Vienna')

    @staticmethod
    def eval(media_file: MediaFile, groups) -> None:
        if len(groups) == 7:
            year, month, day, _, hour, minute, second = groups
            year = int(year)
            month = int(month)
            day = int(day)
            hour = int(hour)
            minute = int(minute)
            second = int(second)

            if year < 85:
                year += 2000
            else:
                year += 1900
            logger.debug(f'year={year}, month={month}, day={day}, '
                         f'hour={hour}, minute={minute}, second={second}')

            ts = datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
                microsecond=0,
                tzinfo=EvalPattern01.TZ
            )
            logger.debug(f'parsed timestamp={ts}')

            media_file.update_time(ts)
            media_file.ts_source = TsSource.FILENAME
