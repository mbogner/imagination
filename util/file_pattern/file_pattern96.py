import re
import zoneinfo
from datetime import datetime

from model.media_file import MediaFile
from model.ts_source import TsSource


class FilePattern96:
    PATTERN = re.compile(r"^(\d\d\d\d)[-_\s](\d\d)[-_\s](\d\d).*")
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
                tzinfo=FilePattern96.TZ
            )

            media_file.update_time(ts, TsSource.FILENAME_YEAR_MONTH_DAY1, True)
