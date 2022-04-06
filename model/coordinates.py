class Coordinates:
    lat: float
    lon: float
    msl: float  # meters above sea level

    def __init__(self, lat: float, lon: float, msl: float):
        self.lat = lat
        self.lon = lon
        self.msl = msl

    def __repr__(self):
        return f'Coordinates[lat={self.lat}, lon={self.lon}, alt={self.msl}]'
