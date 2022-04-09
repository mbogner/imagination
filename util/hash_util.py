import hashlib

from logger import logger
from model.media_file import MediaFile


class HashUtil:

    @staticmethod
    def hash_md5(file: str, blocksize: int = 4096) -> str:
        md5 = hashlib.md5()
        with open(file, "rb") as f:
            for block in iter(lambda: f.read(blocksize), b""):
                md5.update(block)
        return md5.hexdigest()

    @staticmethod
    def hash_files(media_files: list[MediaFile]) -> dict[str, list[MediaFile]]:
        logger.info(f'find duplicates in {len(media_files)} files')
        hash_to_media_file: dict[str, list[MediaFile]] = {}
        for media_file in media_files:
            media_file.md5 = HashUtil.hash_md5(media_file.original_path)
            if media_file.md5 in hash_to_media_file:
                hash_to_media_file[media_file.md5].append(media_file)
            else:
                hash_to_media_file[media_file.md5] = [media_file]
        duplicate_count = len(media_files) - len(hash_to_media_file)
        logger.info(f'found {duplicate_count} duplicates')
        return hash_to_media_file
