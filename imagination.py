import argparse

from config import Config
from logger import logger
from model.match_type import MatchType
from model.media_file import MediaFile
from util.duplicate_resolver import DuplicateResolver
from util.exif_reader import ExifReader
from util.exif_writer import ExifWriter
from util.file_util import FileUtil
from util.hash_util import HashUtil
from util.pattern_parser import PatternParser
from util.unique_filename_util import UniqueFilenameUtil


class App:
    source_dir: str
    target_dir: str
    write_exif: bool
    copy_files: bool

    def __init__(self, source_dir: str, target_dir: str, write_exif: bool = False, copy_files: bool = False):
        self.source_dir = source_dir
        self.target_dir = target_dir

        self.write_exif = write_exif
        if self.write_exif is None:
            self.write_exif = False

        self.copy_files = copy_files
        if self.copy_files is None:
            self.copy_files = False

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

        # translate the hash back to list
        enriched = [item[0] for item in media_hash.values()]
        del media_hash

        # make sure we have unique filenames by adding an index and creating unique filenames based on them
        UniqueFilenameUtil.enrich_indizes(enriched)
        UniqueFilenameUtil.enrich_filenames(enriched, self.target_dir)

        # move over files
        FileUtil.transfer_files(enriched, self.copy_files)

        # write exif to files in target directory
        if self.write_exif:
            ExifWriter.add_exif_to_jpg_if_missing(enriched)

        logger.info('done')


def main():
    logger.info(f"starting {Config.APP_NAME}, v{Config.APP_VERSION}, environment: {Config.APP_ENVIRONMENT}")
    source, target, write_exif, copy_files = parse_arguments()
    App(source, target, write_exif, copy_files).run()


def parse_arguments():
    parser = argparse.ArgumentParser(description="Image archiving utility.")
    parser.add_argument('--source', type=str, help='source directory', required=True)
    parser.add_argument('--target', type=str, help='target directory', required=True)
    parser.add_argument('--write_exif', action=argparse.BooleanOptionalAction, help='write missing exif')
    parser.add_argument('--copy_files', action=argparse.BooleanOptionalAction, help='copy instead of move files to target')
    args = parser.parse_args()
    source = FileUtil.check_directory(args.source, required=True, create=False)
    target = FileUtil.check_directory(args.target, required=False, create=True)
    return source, target, args.write_exif, args.copy_files


if __name__ == "__main__":
    main()
