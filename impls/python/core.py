import printer
from mal_types import MalList, MalAtom, MalException
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

def cons(a, b):
    temp = MalList("(")
    temp.append(a)
    for next_item in b:
        temp.append(next_item)
    return temp

def concat(*a):
    temp = MalList("(")
    for next_list in a:
        for next_item in next_list:
            temp.append(next_item)
    return temp

def vec(a):
    temp = MalList("[")
    temp.extend(a)
    return temp

def nth(a, b):
    try:
        return a[b]
    except IndexError:
        raise MalException("range")

def rest(x):
    temp = MalList("(")
    if x is not None and len(x) > 0:
        temp += x[1:]
    return temp

def throw(x):
    raise MalException(x)

def apply(x, *y):
    assert type(y[-1] == MalList)
    tmp = MalList("(")
    for i in y[:-1]:
        tmp.append(i)
    tmp.extend(y[-1])
    if type(x) == dict:
        return x["fn"](*tmp)
    else:
        return x(*tmp)

def map_(x, y):
    tmp = MalList("(")
    if type(x) == dict:
        x = x["fn"]
    for i in y:
        tmp.append(x(i))
    return tmp

def keyword(x):
    if x[0] == ":":
        return x
    x = x.lstrip('"').rstrip('"')
    return ":" + x

def vector(*x):
    tmp = MalList("[")
    for i in x:
        tmp.append(i)
    return tmp

def to_dict(x):
    assert type(x) == MalList and x.opener == "{"

    for i in range(0, len(x), 2):
        x.dict[x[i]] = x[i + 1]
    
def to_list(x):
    assert x is None or type(x) == MalList and x.opener == "{"

    if x is None:
        return None

    x.clear()
    tmp = []
    for i in sorted(x.dict):
        tmp.append(i)
        tmp.append(x.dict[i])
    x.extend(tmp)

def hash_decor(func):
    def wrapper(*args, **kwargs):
        tmp = func(*args, **kwargs)
        to_dict(tmp)
        to_list(tmp)
        return tmp

    return wrapper

@hash_decor
def hash_map(*x):
    assert len(x) % 2 == 0
    tmp = MalList("{")
    tmp.extend(x)
    return tmp

@hash_decor
def assoc(x, *y):
    assert len(y) % 2 == 0
    assert type(x) == MalList and x.opener == "{"

    tmp = MalList("{")
    tmp_dict = {}

    for i in range(0, len(x), 2):
        tmp_dict[x[i]] = x[i + 1]

    for i in range(0, len(y), 2):
        tmp_dict[y[i]] = y[i + 1]

    for key in tmp_dict:
        tmp.append(key)
        tmp.append(tmp_dict[key])

    return tmp

@hash_decor
def dissoc(x, *y):
    assert type(x) == MalList and x.opener == "{"

    tmp = MalList("{")
    tmp.extend(x)
    for next_key in y:
        idx = -1 
        for i in range(0, len(tmp), 2):
            if tmp[i] == next_key:
                idx = i
                break
        if idx == -1:
            continue
        del tmp[idx:idx+2]

    return tmp

def get(h, k):
    assert (type(h) == MalList and h.opener == "{") or h is None

    if h is None:
        return None

    for i in range(0, len(h), 2):
        if h[i] == k:
            return h[i + 1]
    else:
        return None

def contains(h, k):
    assert type(h) == MalList and h.opener == "{"

    for i in range(0, len(h), 2):
        if h[i] == k:
            return True
    return False

def keys(h):
    assert type(h) == MalList and h.opener == "{"

    tmp = MalList("(")

    for i in range(0, len(h), 2):
        tmp.append(h[i])

    return tmp

def vals(h):
    assert type(h) == MalList and h.opener == "{"

    tmp = MalList("(")

    for i in range(1, len(h), 2):
        tmp.append(h[i])

    return tmp



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
        "cons": cons,
        "concat": concat,
        "vec": vec,
        "nth": nth,
        "first": lambda x: x[0] if x is not None and len(x) > 0 else None,
        "rest": rest,
        "throw": throw,
        "apply": apply,
        "map": map_,
        "nil?": lambda x: x is None,
        "true?": lambda x: x is True,
        "false?": lambda x: x is False,
        "symbol?": lambda x: type(x) == str and x[0] not in ':"',
        "symbol": lambda x: x.lstrip('"').rstrip('"'),
        "keyword": keyword,
        "keyword?": lambda x: type(x) == str and x[0] == ':',
        "vector": vector,
        "vector?": lambda x: type(x) == MalList and x.opener == "[",
        "sequential?": lambda x: type(x) == MalList and x.opener != "{",
        "hash-map": hash_map,
        "map?": lambda x: type(x) == MalList and x.opener == "{",
        "assoc": assoc,
        "dissoc": dissoc,
        "get": get,
        "contains?": contains,
        "keys": keys,
        "vals": vals,
}

