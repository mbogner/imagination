import re
import zoneinfo
from datetime import datetime

from logger import logger
from model.media_file import MediaFile
from model.ts_source import TsSource


class DirPattern01:
    PATTERN = re.compile(r"(\d{4})[-_.]?(\d{2})[-_.]?(\d{2})")
    TZ = zoneinfo.ZoneInfo('Europe/Vienna')
    JOINED = False

    @staticmethod
    def eval(media_file: MediaFile, groups) -> None:
        if len(groups) == 3:
            year, month, day = groups
            year = int(year)
            month = int(month)
            day = int(day)

            logger.debug(f'year={year}, month={month}, day={day}')

            ts = datetime(
                year=year,
                month=month,
                day=day,
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=DirPattern01.TZ
            )
            logger.debug(f'parsed timestamp={ts}')

            media_file.update_time(ts)
            media_file.ts_source = TsSource.DIR1
