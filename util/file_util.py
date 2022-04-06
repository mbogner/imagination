import glob

from config import Config
from logger import logger
from model.media_file import MediaFile


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
