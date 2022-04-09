from datetime import datetime, timezone

from config import Config
from logger import logger
from model.coordinates import Coordinates
from model.media_type import MediaType
from model.ts_source import TsSource


class MediaFile:
    original_path: str
    original_filename: str
    filename: str
    media_type: MediaType
    dir_path: list[str]

    unix_time_sec: int = None
    timestamp: datetime = None
    ts_source: TsSource = None
    mtime: datetime = None
    index: int = None

    coordinates: Coordinates = None

    md5: str = None

    target_dir = None
    target_filename = None
    target = None

    def __init__(self, original_path: str, original_filename: str, filename: str, media_type: MediaType,
                 dir_path: list[str]):
        self.original_path = original_path
        self.original_filename = original_filename
        self.filename = filename
        self.media_type = media_type
        self.dir_path = dir_path

    def __repr__(self):
        if self.ts_source == TsSource.EXIF:
            sym = Config.SYM_CHECK
        else:
            sym = Config.SYM_MULTIPLICATION
        return f'{sym} {self.ts_source} {self.dir_path}/{self.original_filename}, ts={self.timestamp}'

    def __lt__(self, other):
        return self.original_filename.lower() < other.original_filename.lower()

    def has_timestamp(self) -> bool:
        return self.timestamp is not None

    def update_time(self, ts: datetime, source: TsSource, force: bool = False):
        if ts is not None and (force or self.timestamp is None or ts < self.timestamp):
            self.timestamp = ts.astimezone(timezone.utc)
            self.unix_time_sec = int(self.timestamp.timestamp())
            self.ts_source = source
            if self.ts_source == TsSource.MTIME:
                self.mtime = ts

    def update_coordinates(self, coordinates: Coordinates):
        if coordinates is not None:
            self.coordinates = coordinates

    @staticmethod
    def create(source_dir: str, file_dir: str) -> 'MediaFile':
        original_filename, filename, media_type, split_path = MediaFile.retrieve_filename_data(source_dir, file_dir)
        return MediaFile(
            original_path=file_dir,
            original_filename=original_filename,
            filename=filename,
            media_type=media_type,
            dir_path=split_path
        )

    @staticmethod
    def retrieve_filename_data(source_dir: str, file_dir: str):
        if not source_dir.endswith('/'):
            source_dir += '/'

        split_path = file_dir.replace(source_dir, '').split('/')
        original_filename = split_path.pop()
        fixed_filename = MediaFile.replace_dots(original_filename)
        filename, extension = fixed_filename.split('.')
        media_type = MediaType.from_string(extension)

        return original_filename, filename, media_type, split_path

    @staticmethod
    def replace_dots(original_filename: str) -> str:
        result = original_filename
        while result.count('.') > 1:
            result = result.replace('.', ' ', 1)
        return result
