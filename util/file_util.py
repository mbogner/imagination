import glob
import os
from datetime import datetime

from config import Config
from logger import logger
from model.media_file import MediaFile
from model.ts_source import TsSource
from util.date_time_util import DateTimeUtil


class FileUtil:

    @staticmethod
    def slurp_filenames(source_dir) -> list[MediaFile]:
        logger.info(f"reading all filenames into memory")
        media_files: list[MediaFile] = []
        for pattern in Config.FILE_PATTERNS:
            for file in glob.glob(f'{source_dir}/{pattern}', recursive=True):
                media_files.append(MediaFile.create(source_dir, file))
        logger.info(f"filename(s) prepared: {len(media_files)}")
        return media_files

    @staticmethod
    def delete_all_files(files: list[MediaFile]) -> None:
        for file in files:
            os.remove(file.original_path)

    @staticmethod
    def get_last_file_change_ts(file) -> datetime:
        mtime: float = os.path.getmtime(file)
        ts = DateTimeUtil.parse_unix_time_sec(int(mtime))
        return ts

    @staticmethod
    def enrich_from_file_mtime(files: list[MediaFile]) -> None:
        for file in files:
            file.update_time(FileUtil.get_last_file_change_ts(file.original_path), TsSource.MTIME)

    @staticmethod
    def join_path(folders: list[str], separator: str = ' ') -> str:
        return separator.join(folders)
