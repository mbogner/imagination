from logger import logger
from model.media_file import MediaFile


class DuplicateResolver:

    @staticmethod
    def dedup(media_hash: dict[str, list[MediaFile]]) -> None:
        logger.info('dedup files')
        for key, media_file_list in media_hash.items():
            if len(media_file_list) < 2:
                continue
            oldest = media_file_list[0]
            for media_file in media_file_list:
                if media_file.timestamp < oldest.timestamp:
                    oldest = media_file
            media_hash[key] = [oldest]
