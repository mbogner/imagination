import glob

from config import Config
from logger import logger
from model.media_file import MediaFile
from util.string_util import parse_arguments


class App:
    source_dir: str
    target_dir: str

    def __init__(self, source_dir: str, target_dir: str):
        self.source_dir = source_dir
        self.target_dir = target_dir

    def run(self):
        logger.debug(f"source_dir={self.source_dir}, target_dir={self.target_dir}")
        media = self.slurp_filenames()

    def slurp_filenames(self) -> list[MediaFile]:
        logger.info(f"reading all filenames into memory")
        patterns = [
            f'{self.source_dir}/**/*.[jJ][pP][gG]',
            f'{self.source_dir}/**/*.[jJ][pP][eE][gG]',
            f'{self.source_dir}/**/*.[mM][oO][vV]',
        ]
        media_files: list[MediaFile] = []
        for pattern in patterns:
            for file in glob.glob(pattern, recursive=True):
                media_files.append(MediaFile.create(self.source_dir, file))
        logger.info(f"filename(s) prepared: {len(media_files)}")
        return media_files


def main():
    logger.info(f"starting {Config.APP_NAME}, v{Config.APP_VERSION}, environment: {Config.APP_ENVIRONMENT}")
    source, target = parse_arguments()
    App(source, target).run()
    logger.info('done')


if __name__ == "__main__":
    main()
