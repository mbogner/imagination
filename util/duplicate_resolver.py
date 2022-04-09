import os

from logger import logger
from model.media_file import MediaFile
from model.ts_source import TsSource


class DuplicateResolver:

    @staticmethod
    def dedup(media_hash: dict[str, list[MediaFile]], delete_duplicates: bool = False) -> None:
        logger.info('dedup files')
        for key, media_file_list in media_hash.items():
            if len(media_file_list) < 2:
                continue
            selected = media_file_list[0]
            for media_file in media_file_list:
                if media_file.ts_source == TsSource.EXIF or media_file.timestamp < selected.timestamp:
                    selected = media_file
            if delete_duplicates:
                for media_file in media_file_list:
                    if media_file != selected:
                        os.remove(media_file.original_path)

            media_hash[key] = [selected]

        logger.info('dedup files done')
