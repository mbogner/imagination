from logger import logger
from model.match_type import MatchType
from model.media_file import MediaFile
from util.dir_pattern.dir_pattern01 import DirPattern01
from util.file_pattern.file_pattern01 import FilePattern01
from util.file_pattern.file_pattern02 import FilePattern02
from util.file_util import FileUtil


class PatternParser:
    FILE_PATTERNS = [FilePattern01, FilePattern02]
    DIR_PATTERNS = [DirPattern01]

    @staticmethod
    def update_from_pattern(media_files: list[MediaFile], match_type: MatchType) -> None:
        logger.info('enriching media files from patterns')
        for media_file in media_files:
            if media_file.timestamp is not None:
                continue

            if match_type == MatchType.FILE:
                mapping = PatternParser.FILE_PATTERNS
            elif match_type == MatchType.DIR:
                mapping = PatternParser.DIR_PATTERNS
                if media_file.dir_path is None or len(media_file.dir_path) < 1:
                    continue
            else:
                raise Exception(f'unknown match_type: {match_type}')

            for impl in mapping:
                if match_type == MatchType.FILE:
                    match = impl.PATTERN.match(media_file.filename)
                elif match_type == MatchType.DIR:
                    # noinspection PyUnresolvedReferences
                    # this reference is known for DIR
                    if impl.JOINED:
                        joined = FileUtil.join_path(media_file.dir_path, '/')
                        match = impl.PATTERN.match(joined)
                    else:
                        match = impl.PATTERN.match(media_file.dir_path[0])
                else:
                    raise Exception(f'unknown match_type: {match_type}')
                if match is None:
                    continue
                impl.eval(media_file, match.groups())
