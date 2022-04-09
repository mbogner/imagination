class StringUtil:

    @staticmethod
    def expand_to_len(orig: int, wanted_len: int, prefix: str = '0', postfix: str = '') -> str:
        res = f"{orig}"
        while len(res) < wanted_len:
            res = f"{prefix}{res}{postfix}"
        return res
