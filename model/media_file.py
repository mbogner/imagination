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

    coordinates: Coordinates = None

    def __init__(self, original_path: str, original_filename: str, filename: str, media_type: MediaType,
                 dir_path: list[str]):
        self.original_path = original_path
        self.original_filename = original_filename
        self.filename = filename
        self.media_type = media_type
        self.dir_path = dir_path

    def __repr__(self):
        if self.has_timestamp():
            return f'{Config.SYM_CHECK} {self.dir_path} {self.filename}.{self.media_type}, ' \
                   f'ts={self.timestamp}, ts_source={self.ts_source}'
        else:
            return f'{Config.SYM_MULTIPLICATION} {self.dir_path} {self.filename}.{self.media_type}'

    def has_timestamp(self) -> bool:
        return self.timestamp is not None

    def update_time(self, ts: datetime):
        if ts is not None:
            self.timestamp = ts.astimezone(timezone.utc)
            self.unix_time_sec = int(self.timestamp.timestamp())

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
        logger.debug(f"splitting file_dir={file_dir}")
        if not source_dir.endswith('/'):
            source_dir += '/'

        split_path = file_dir.replace(source_dir, '').split('/')
        original_filename = split_path.pop()
        fixed_filename = MediaFile.replace_dots(original_filename)
        filename, extension = fixed_filename.split('.')
        media_type = MediaType.from_string(extension)

        logger.debug(f'split result: original_filename={original_filename}, filename={filename}, '
                     f'media_type={media_type}, split_path={split_path}')
        return original_filename, filename, media_type, split_path

    @staticmethod
    def replace_dots(original_filename: str) -> str:
        result = original_filename
        while result.count('.') > 1:
            result = result.replace('.', ' ', 1)
        return result
