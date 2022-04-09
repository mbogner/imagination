from config import Config
from logger import logger
from model.match_type import MatchType
from model.media_file import MediaFile
from model.ts_source import TsSource
from util.duplicate_resolver import DuplicateResolver
from util.exif_reader import ExifReader
from util.file_util import FileUtil
from util.hash_util import HashUtil
from util.pattern_parser import PatternParser
from util.string_util import parse_arguments
from util.unique_filename_util import UniqueFilenameUtil


class App:
    source_dir: str
    target_dir: str

    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = source_dir
        self.target_dir = target_dir

    def run(self):
        logger.debug(f"source_dir={self.source_dir}, target_dir={self.target_dir}")
        media: list[MediaFile] = FileUtil.slurp_filenames(self.source_dir)
        FileUtil.enrich_from_file_mtime(media)
        PatternParser.update_from_pattern(media, MatchType.DIR)
        PatternParser.update_from_pattern(media, MatchType.FILE)
        ExifReader.enrich_with_exif_data(media)
        # non_exif = [item for item in media if item.ts_source != TsSource.EXIF]

        # create md5 of all files and get rid of duplicates
        media_hash = HashUtil.hash_files(media)
        del media  # use the new hash from now
        DuplicateResolver.dedup(media_hash)

        enriched = [item[0] for item in media_hash.values()]
        del media_hash
        UniqueFilenameUtil.enrich_indizes(enriched)
        UniqueFilenameUtil.enrich_filenames(enriched)

        logger.info('done')


def main():
    logger.info(f"starting {Config.APP_NAME}, v{Config.APP_VERSION}, environment: {Config.APP_ENVIRONMENT}")
    source, target = parse_arguments()
    App(source, target).run()


if __name__ == "__main__":
    main()
