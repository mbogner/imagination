import re
import zoneinfo
from datetime import datetime

from logger import logger
from model.media_file import MediaFile
from model.ts_source import TsSource


class DirPattern03:
    PATTERN = re.compile(r"^(\d{4}).*")
    TZ = zoneinfo.ZoneInfo('Europe/Vienna')
    JOINED = False

    @staticmethod
    def eval(media_file: MediaFile, groups) -> None:
        if len(groups) == 1:
            year = groups[0]
            year = int(year)

            ts = datetime(
                year=year,
                month=12,
                day=31,
                hour=12,
                minute=0,
                second=0,
                microsecond=0,
                tzinfo=DirPattern03.TZ
            )
            media_file.update_time(ts, TsSource.DIR_YEAR)
