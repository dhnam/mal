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

class MalAtom:
    def __init__(self, value):
        self.value = value

