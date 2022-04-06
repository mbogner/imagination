from enum import Enum, auto


class TsSource(Enum):
    EXIF = auto()
    FILENAME1 = auto()
    FILENAME2 = auto()
    DIR1 = auto()
    MTIME = auto()
    FOLDER = auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
