class NotFoundException(Exception):
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg
class Env:
    pass
class Env:
    def __init__(self, outer: Env):
        self.outer = outer
        self.data = {}

    def set_(self, key, value):
        self.data[key] = value

    def find(self, key):
        if key in self.data:
            return self
        elif self.outer is not None: # not nil; I'll write it None for now
            return self.outer.find(key)
       
    def get(self, key):
        env_key = self.find(key)
        if env_key is not None:
            return env_key.data[key]
        
        raise NotFoundException(key)


