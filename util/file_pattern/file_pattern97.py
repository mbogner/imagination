import re
import zoneinfo
from datetime import datetime

from model.media_file import MediaFile
from model.ts_source import TsSource


class FilePattern97:
    PATTERN = re.compile(r"[-_a-zA-Z\s]*[-_](\d\d\d\d)(\d\d)(\d\d)[-_].*")
    TZ = zoneinfo.ZoneInfo('Europe/Vienna')

    @staticmethod
    def eval(media_file: MediaFile, groups) -> None:
        if len(groups) == 3:
            year, month, day = groups
            year = int(year)
            month = int(month)
            day = int(day)

            ts = datetime(
                year=year,
                month=month,
                day=day,
                hour=12,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=FilePattern97.TZ
            )

            media_file.update_time(ts, TsSource.FILENAME_YEAR_MONTH_DAY2, True)
