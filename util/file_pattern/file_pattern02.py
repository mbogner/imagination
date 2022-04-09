import re
import zoneinfo
from datetime import datetime

from logger import logger
from model.media_file import MediaFile
from model.ts_source import TsSource


class FilePattern02:
    PATTERN = re.compile(
        r".*(\d{2}?\d{2})(\d{2})(\d{2})[-_\s](\d{2})(\d{2})(\d{2})[.].*"
    )
    TZ = zoneinfo.ZoneInfo('Europe/Vienna')

    @staticmethod
    def eval(media_file: MediaFile, groups) -> None:
        if len(groups) == 6:
            year, month, day, hour, minute, second = groups
            year = int(year)
            month = int(month)
            day = int(day)
            hour = int(hour)
            minute = int(minute)
            second = int(second)

            if year < 1900:
                if year < 85:
                    year += 2000
                else:
                    year += 1900

            ts = datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
                microsecond=0,
                tzinfo=FilePattern02.TZ
            )

            media_file.update_time(ts, TsSource.FILENAME2, True)
