import calendar
import re
import zoneinfo
from datetime import datetime

from logger import logger
from model.media_file import MediaFile
from model.ts_source import TsSource


class FilePattern98:
    PATTERN = re.compile(r"^(\d\d\d\d)[-_.\s](\d\d).*")
    TZ = zoneinfo.ZoneInfo('Europe/Vienna')

    @staticmethod
    def eval(media_file: MediaFile, groups) -> None:
        if len(groups) == 2:
            year, month = groups
            year = int(year)
            month = int(month)

            ts = datetime(
                year=year,
                month=month,
                day=calendar.monthrange(year, month)[1],
                hour=12,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=FilePattern98.TZ
            )
            media_file.update_time(ts, TsSource.FILENAME_YEAR_MONTH2, True)
