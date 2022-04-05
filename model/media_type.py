from enum import Enum, unique, auto


@unique
class MediaType(Enum):
    JPG = auto()
    MOV = auto()

    @staticmethod
    def from_string(val: str):
        val = val.lower()
        if val == 'jpg' or val == 'jpeg':
            return MediaType.JPG
        if val == 'mov':
            return MediaType.MOV
        raise f'invalid media type: {val}'

    def __str__(self):
        return self.name.lower()

    def __repr__(self):
        return self.name
