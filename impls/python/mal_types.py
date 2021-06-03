class MalList(list):
    bracket_pair = {
        "(": ")",
        "[": "]",
        "{": "}",
            }
    def __init__(self, opener="", *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.opener = opener
        self.closer = MalList.bracket_pair[opener]
        if opener == "{":
            self.dict = {} # cheap monkey patch, as always :D

    def __eq__(self, other):
        try:
            return super().__eq__(other) and\
                    ((self.opener in "([" and other.opener in "([") or self.opener == other.opener == "{")
        except AttributeError:
            return False

class MalAtom:
    def __init__(self, value):
        self.value = value

class MalException(Exception):
    pass
