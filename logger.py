import logging.config
import sys

from config import Config

logging.basicConfig(format=Config.LOG_FORMAT, level=Config.LOG_LEVEL, stream=sys.stdout)
logger = logging.getLogger()

libraries = {
    'config': logging.WARNING,
}
for library, level in libraries.items():
    library_logger = logging.getLogger(library)
    library_logger.setLevel(level)
    library_logger.propagate = False
