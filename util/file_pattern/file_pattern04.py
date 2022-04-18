import re
import zoneinfo
from datetime import datetime

from model.media_file import MediaFile
from model.ts_source import TsSource


class FilePattern04:
    PATTERN = re.compile(r"^(\d\d\d\d)[-_\s](\d\d)[-_\s](\d\d)[-_\s]+(\d\d)[-_:\s](\d\d)[-_:\s](\d\d).*")
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

            ts = datetime(
                year=year,
                month=month,
                day=day,
                hour=hour,
                minute=minute,
                second=second,
                microsecond=0,
                tzinfo=FilePattern04.TZ
            )

            media_file.update_time(ts, TsSource.FILENAME3, True)
