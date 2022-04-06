import calendar
from datetime import datetime, timezone, timedelta


class DateTimeUtil:

    @staticmethod
    def now_utc() -> datetime:
        return datetime.now(timezone.utc)

    @staticmethod
    def parse_unix_time_sec(unix_time_sec: int) -> datetime:
        ts = datetime.fromtimestamp(unix_time_sec)
        return ts.replace(tzinfo=timezone.utc)

    @staticmethod
    def parse_unix_time_sec_str(unix_time_sec: str) -> datetime:
        return DateTimeUtil.parse_unix_time_sec(int(unix_time_sec))

    @staticmethod
    def last_sunday_of_month(year: int, month: int):
        m = calendar.monthcalendar(year, month)
        return max(m[-1][calendar.SUNDAY], m[-2][calendar.SUNDAY])

    @staticmethod
    def last_sunday_of_month_from_ts(ts: datetime):
        m = calendar.monthcalendar(ts.year, ts.month)
        return max(m[-1][calendar.SUNDAY], m[-2][calendar.SUNDAY])

    @staticmethod
    def timezone_datetime(ts: datetime) -> datetime:
        h_offset = 0
        ts = ts.replace(tzinfo=timezone.utc)
        if 3 < ts.month < 10:  # must be CET
            h_offset = 2
        elif ts.month < 3 or ts.month > 10:  # must be CEST
            h_offset = 1
        elif ts.month == 3:  # check CEST or CET
            last_sunday = DateTimeUtil.last_sunday_of_month_from_ts(ts)
            if (ts.day == last_sunday and ts.hour >= 2) or ts.day > last_sunday:
                h_offset = 2
            else:
                h_offset = 1
        elif ts.month == 10:  # check CEST or CET
            last_sunday = DateTimeUtil.last_sunday_of_month_from_ts(ts)
            if (ts.day == last_sunday and ts.hour >= 3) or ts.day > last_sunday:
                h_offset = 1
            else:
                h_offset = 2
        return ts.replace(tzinfo=timezone(timedelta(hours=h_offset)))
