import glob
import os
import pathlib
import shutil
import sys
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

    @staticmethod
    def check_directory(path: str, required: bool = False, create: bool = False, exit_code: int = 3):
        if not os.path.isdir(path):
            if required:
                print(f'required directory {path} does not exist')
                sys.exit(exit_code)
            if create:
                pathlib.Path(path).mkdir(parents=True, exist_ok=True)
        return os.path.abspath(path)

    @staticmethod
    def transfer_files(media_files: list[MediaFile], copy_files: bool) -> None:
        """
        Transfer files from media_file.original_path to media_file.target.
        :param media_files: list of MediaFile.
        :param copy_files: When True files are copied instead of moved.
        :return: None
        """
        logger.info(f"moving files, copy_files={copy_files}")
        for media_file in media_files:
            FileUtil.check_directory(media_file.target_dir, required=False, create=True)
            # ignore existing
            if os.path.isfile(media_file.target):
                os.remove(media_file.original_path)
                continue
            if copy_files:
                shutil.copy(media_file.original_path, media_file.target)
            else:
                shutil.move(media_file.original_path, media_file.target)
        logger.info("moving files done")
