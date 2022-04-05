import argparse
import os
import pathlib
import sys

from logger import logger


def check_directory(path: str, required: bool = False, create: bool = False):
    logger.debug(f'testing for directory {path} (required={required}, create={create})')
    if not os.path.isdir(path):
        if required:
            print(f'required directory {path} does not exist')
            sys.exit(3)
        if create:
            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
    return os.path.abspath(path)


def parse_arguments():
    parser = argparse.ArgumentParser(description="Image archiving utility.")
    parser.add_argument('--source', metavar='s', type=str, help='source directory')
    parser.add_argument('--target', metavar='t', type=str, help='target directory')
    args = parser.parse_args()
    source = check_directory(args.source, required=True, create=False)
    target = check_directory(args.target, required=False, create=True)
    return source, target
