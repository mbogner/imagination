from datetime import datetime, timezone

import pytest

from util.exif_writer import ExifWriter


class TestExifWriter:

    @pytest.mark.parametrize('ts', [
        datetime(
            year=2022,
            month=3,
            day=20,
            hour=12,
            minute=45,
            second=13,
            microsecond=0,
            tzinfo=timezone.utc
        )
    ])
    def test_translate_utc_to_exif(self, ts):
        result: dict = ExifWriter.translate_utc_to_exif(ts)
        assert result is not None
        assert 'Exif' in result
