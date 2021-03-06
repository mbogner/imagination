import re
import zoneinfo
from datetime import datetime

from model.media_file import MediaFile
from model.ts_source import TsSource


class FilePattern01:
    # /2022-02-14_11-00-00_i000
    PATTERN = re.compile(
        r"^(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})_i(\d{3})[.].*"
    )
    TZ = zoneinfo.ZoneInfo('Europe/Vienna')

    @staticmethod
    def eval(media_file: MediaFile, groups) -> None:
        if len(groups) == 7:
            year, month, day, hour, minute, second, index = groups
            year = int(year)
            month = int(month)
            day = int(day)
            hour = int(hour)
            minute = int(minute)
            second = int(second)
            index = int(index)

            ts = datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
                microsecond=0,
                tzinfo=FilePattern01.TZ
            )

            media_file.update_time(ts, TsSource.FILENAME1, True)
            media_file.index = index
