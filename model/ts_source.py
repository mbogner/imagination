from enum import Enum, auto


class TsSource(Enum):
    EXIF = auto()
    FILENAME = auto()

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
