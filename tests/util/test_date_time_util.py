from datetime import datetime, timezone, timedelta

import pytest

from util.date_time_util import DateTimeUtil


class TestDateTimeUtil:

    def test_last_sunday_of_month_from_ts(self):
        result = DateTimeUtil.last_sunday_of_month_from_ts(datetime(
            year=2022, month=3, day=1,
            hour=0, minute=0, second=0, microsecond=0
        ))
        assert result == 27

    def test_last_sunday_of_month(self):
        result = DateTimeUtil.last_sunday_of_month(2022, 3)
        assert result == 27

    @pytest.mark.parametrize('hour, tz', ((1, 1), (2, 2)))
    def test_timezone_datetime(self, hour: int, tz: int):
        result = DateTimeUtil.timezone_datetime(datetime(
            year=2022, month=3, day=27,
            hour=hour, minute=0, second=0, microsecond=0
        ))
        assert result is not None
        assert result.tzinfo == timezone(timedelta(hours=tz))

    @pytest.mark.parametrize('unix, year', ((0, 1970), (1649279523, 2022)))
    def test_parse_unix_time_sec(self, unix: int, year: int):
        ts = DateTimeUtil.parse_unix_time_sec(unix)
        assert ts.year == year
