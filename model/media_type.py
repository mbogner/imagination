from enum import Enum, unique, auto


@unique
class MediaType(Enum):
    JPG = auto()
    MOV = auto()
    PNG = auto()
    MP4 = auto()
    ARW = auto()
    AVI = auto()
    HEIC = auto()

    @staticmethod
    def from_string(val: str):
        val = val.lower()
        if val == 'jpg' or val == 'jpeg':
            return MediaType.JPG
        if val == 'mov':
            return MediaType.MOV
        if val == 'png':
            return MediaType.PNG
        if val == 'mp4':
            return MediaType.MP4
        if val == 'avi':
            return MediaType.AVI
        if val == 'arw':
            return MediaType.ARW
        if val == 'heic':
            return MediaType.HEIC
        raise Exception(f'invalid media type: {val}')

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return self.name.lower()
