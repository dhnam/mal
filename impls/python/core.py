import printer
from mal_types import MalList, MalAtom
import reader

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

def slurp(file_name):
    with open(file_name[1:-1], "r") as f:
        str_file = f.read()
    return '"' + str_file + '"'

def reset(atom, val):
    atom.value = val
    return val

def swap(atom, func, *args):
    if type(func) == type(lambda x: None):
        atom.value = func(atom.value, *args)
        return atom.value
    else:
        atom.value = func["fn"](atom.value, *args)
        return atom.value

def read_str(x):
    try:
        return reader.read_str(x[1:-1])
    except reader.NoTokenException:
        return None


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
        "read-string": read_str,
        "slurp": slurp,
        "atom": lambda x: MalAtom(x),
        "atom?": lambda x: type(x) == MalAtom,
        "deref": lambda x: x.value,
        "reset!": reset,
        "swap!": swap,
      }

