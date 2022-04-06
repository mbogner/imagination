import orjson


class Var:

    @staticmethod
    def to_bool(var):
        if var is None:
            return None
        return bool(orjson.loads(str(var).lower()))
