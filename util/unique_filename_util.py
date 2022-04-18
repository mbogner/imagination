from logger import logger
from model.media_file import MediaFile
from util.string_util import StringUtil


class UniqueFilenameUtil:

    @staticmethod
    def enrich_filenames(media_files: list[MediaFile], target_base_dir: str) -> None:
        for media_file in media_files:
            ts = media_file.timestamp
            media_file.target_dir = f"{target_base_dir}/{ts.year}/{StringUtil.expand_to_len(ts.month, 2)}"
            media_file.target_filename = f"{ts.year}-" \
                                         f"{StringUtil.expand_to_len(ts.month, 2)}-" \
                                         f"{StringUtil.expand_to_len(ts.day, 2)}_" \
                                         f"{StringUtil.expand_to_len(ts.hour, 2)}-" \
                                         f"{StringUtil.expand_to_len(ts.minute, 2)}-" \
                                         f"{StringUtil.expand_to_len(ts.second, 2)}_" \
                                         f"i{StringUtil.expand_to_len(media_file.index, 3)}" \
                                         f".{media_file.media_type}"
            media_file.target = f'{media_file.target_dir}/{media_file.target_filename}'

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
