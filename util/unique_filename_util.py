from logger import logger
from model.media_file import MediaFile
from util.string_util import expand_to_len


class UniqueFilenameUtil:

    @staticmethod
    def enrich_filenames(media_files: list[MediaFile]) -> None:
        for media_file in media_files:
            ts = media_file.timestamp
            media_file.target_dir = f"{ts.year}/{expand_to_len(ts.month, 2)}"
            media_file.target_filename = f"{ts.year}-" \
                                         f"{expand_to_len(ts.month, 2)}-" \
                                         f"{expand_to_len(ts.day, 2)}_" \
                                         f"{expand_to_len(ts.hour, 2)}-" \
                                         f"{expand_to_len(ts.minute, 2)}-" \
                                         f"{expand_to_len(ts.second, 2)}_" \
                                         f"i{expand_to_len(media_file.index, 3)}.{media_file.media_type}"

    @staticmethod
    def enrich_indizes(media_files: list[MediaFile]) -> None:
        logger.info("adding indizes to media")
        result: dict[int, list[MediaFile]] = {}
        for media_file in media_files:
            if media_file.unix_time_sec in result:
                existing = result[media_file.unix_time_sec]
                media_file.index = len(existing)
                existing.append(media_file)
            else:
                media_file.index = 0
                result[media_file.unix_time_sec] = [media_file]
        logger.info("adding indizes to media done")
