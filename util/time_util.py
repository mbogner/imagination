from datetime import datetime, timezone


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
