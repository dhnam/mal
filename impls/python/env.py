from mal_types import MalList, MalException

class NotFoundException(MalException):
    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self):
        return self.msg

class Env:
    pass
class Env:
    def __init__(self, outer: Env, binds=None, exprs=None):
        if binds is None:
            binds = []
        if exprs is None:
            exprs = []
            
        self.outer = outer
        self.data = {}
        for i in range(len(binds)):
            if binds[i] == "&":
                rest_exprs = MalList("(")
                rest_exprs.extend(exprs[i:])
                self.data[binds[i + 1]] = rest_exprs
                break
            self.data[binds[i]] = exprs[i]

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
        
        raise NotFoundException("\"'" + key + "' not found\"")


