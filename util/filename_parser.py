import re

from logger import logger
from model.media_file import MediaFile
from util.file_pattern.pattern01 import EvalPattern01


class FilenameParser:
    PATTERNS = [
        [re.compile(r".*(\d\d).(\d\d).(\d\d)\s*(at|[Tt ])?\s*(\d\d).(\d\d).(\d\d).*"), EvalPattern01.eval]
    ]

    @staticmethod
    def update_from_filename(media_files: list[MediaFile]) -> None:
        logger.info('enriching media files from filename')
        for media_file in media_files:
            if media_file.timestamp is not None:
                continue
            logger.debug(f"checking file: {media_file}")
            i = -1
            for pattern, method in FilenameParser.PATTERNS:
                i += 1
                match = pattern.match(media_file.filename)
                if match is None:
                    continue
                groups = match.groups()
                if i == 0:
                    method(media_file, groups)
                    continue
                else:
                    raise f'no eval pattern method for index {i}'
