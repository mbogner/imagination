from config import Config
from logger import logger
from model.media_file import MediaFile
from util.exif_reader import ExifReader
from util.file_util import FileUtil
from util.filename_parser import FilenameParser
from util.string_util import parse_arguments


class App:
    source_dir: str
    target_dir: str

    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = source_dir
        self.target_dir = target_dir

    def run(self):
        logger.debug(f"source_dir={self.source_dir}, target_dir={self.target_dir}")
        media: list[MediaFile] = FileUtil.slurp_filenames(self.source_dir)
        ExifReader.enrich_with_exif_data(media)
        FilenameParser.update_from_filename(media)
        logger.info('done')


def main():
    logger.info(f"starting {Config.APP_NAME}, v{Config.APP_VERSION}, environment: {Config.APP_ENVIRONMENT}")
    source, target = parse_arguments()
    App(source, target).run()


if __name__ == "__main__":
    main()
