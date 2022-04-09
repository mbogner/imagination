from enum import Enum, auto


class TsSource(Enum):
    EXIF = auto()
    FILENAME1 = auto()
    FILENAME2 = auto()
    FILENAME3 = auto()
    FILENAME_YEAR_MONTH_DAY1 = auto()
    FILENAME_YEAR_MONTH_DAY2 = auto()
    FILENAME_YEAR_MONTH2 = auto()
    FILENAME_YEAR = auto()
    DIR_YEAR_MONTH_DAY = auto()
    DIR_YEAR_MONTH = auto()
    DIR_YEAR = auto()
    MTIME = auto()
    FOLDER = auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
