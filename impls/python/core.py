import printer
from mal_types import MalList

def list_fn(*x):
    lst = MalList("(")
    lst.extend(x)
    return lst

def count(*x):
    try:
        return len(x[0])
    except TypeError:
        return 0

def strings(join=" ", print_readably=True, make_str=False):
    def inner(*x):
        if len(x) == 0:
            print_str = ''
        else:
            print_str = join.join([printer.pr_str(a, print_readably) for a in x])
        if make_str:
            print_str = '"' + print_str + '"'
        return print_str
    return inner

def print_(join=" ", print_readably=True):
    def inner(*x):
        print(strings(join, print_readably)(*x))
        return None
    return inner

ns = {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x // y,
        "pr-str": strings(make_str=True),
        "str": strings("", False, True),
        "prn": print_(),
        "println": print_(" ", False),
        "list": list_fn,
        "list?": lambda *x: type(x[0]) == MalList and x[0].opener=='(',
        "empty?": lambda *x: len(x[0]) == 0,
        "count": count,
        "=": lambda x, y: x==y,
        "<": lambda x, y: x<y,
        "<=": lambda x, y: x<=y,
        ">": lambda x, y: x>y,
        ">=": lambda x, y: x>=y,
      }
