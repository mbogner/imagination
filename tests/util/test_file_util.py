from datetime import timezone

import pytest

from util.file_util import FileUtil


class TestFileUtil:

    @pytest.mark.parametrize('file', ('/etc/hosts', '/etc/profile'))
    def test_get_last_file_change_ts(self, file: str):
        ts = FileUtil.get_last_file_change_ts(file)
        assert ts is not None
        assert ts.tzinfo == timezone.utc
        assert ts.year > 1970

    @pytest.mark.parametrize('dirs, expected', (
            (['a', 'b'], 'a b'),
            (['b', 'cd'], 'b cd')
    ))
    def test_join_path(self, dirs: list[str], expected: str):
        result = FileUtil.join_path(dirs)
        assert result == expected
