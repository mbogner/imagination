import os

from util.var import Var


class Config:
    APP_NAME = os.environ.get('APP_NAME', 'imagination')
    APP_ENVIRONMENT = os.environ.get('APP_ENVIRONMENT', 'dev')
    APP_VERSION = os.environ.get('APP_VERSION', '1.0.0')
    DEFAULT_ENCODING = 'utf-8'

    # LOGGING
    # --------------------------------------------------------------------------
    # possible: CRITICAL, ERROR, WARNING, INFO, DEBUG, NOTSET
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')
    LOG_FORMAT = os.environ.get(
        'LOG_FORMAT',
        '%(asctime)s %(levelname)s [%(threadName)s,%(name)s] %(filename)s:%(lineno)d - %(message)s'
    )

    SYM_CHECK = '✓'
    SYM_MULTIPLICATION = '✕'

    FILE_PATTERNS = [
        '/**/*.[jJ][pP][gG]',
        '/**/*.[jJ][pP][eE][gG]',
        '/**/*.[mM][oO][vV]',
        '/**/*.[pP][nN][gG]',
        '/**/*.[mM][pP]4',
    ]

    DELETE_DUPLICATES = Var.to_bool(os.environ.get('DELETE_DUPLICATES', 'false'))
