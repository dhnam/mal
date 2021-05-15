import re
import mal_types

class Reader:
    def __init__(self, tokens=None, position=0):
        if (tokens == None):
            self.tokens = []
        else:
            self.tokens = tokens
        self.position = position

    def next(self):
        val = self.peek()
        self.position += 1
        return val

    def __next__(self):
        try:
            return self.next()
        except IndexError:
            raise StopIteration

    def __iter__(self):
        return self

    def peek(self):
        return self.tokens[self.position]

    def __len__(self):
        return len(self.tokens)

def read_str(string):
    tokens = tokenize(string)
    return read_form(Reader(tokens))

def tokenize(string):
    mal_pattern = r'[\s,]*(~@|[\[\]{}()\'`~^@]|"(?:\\.|[^\\"])*"?|;.*|[^\s\[\]{}(\'"`,;)]*)' 
    return [x for x in re.split(mal_pattern, string) if x != '']

def read_form(reader: Reader):
    token = reader.peek()
    if token in "([{":
        return read_list(reader, token)
    else:
        return read_atom(reader)

def read_list(reader: Reader, opener):
    res = mal_types.MalList(opener)
    try:
        for i in reader:
            next_atom = read_form(reader)
            if next_atom == res.closer:
                break
            res.append(next_atom)
    except IndexError:
        raise EOFError
    return res

def escape(string):
    escaped = False
    res = ""
    for s in string:
        if not escaped:
            if s == '\\':
                escaped = True
            else:
                res += s
        else:
            if s == '"':
                res += s
            elif s == "n":
                res += "\n"
            elif s == "\\":
                res += "\\"
            else:
                res += "\\"
                res += s
            escaped = False
    return res

def read_atom(reader: Reader):
    atom = reader.peek()

    special_chars = {
                        "'": "quote",
                        "`": "quasiquote",
                        "~": "unquote",
                        "~@": "splice-unquote",
                        "@": "deref"
                    }
    
    if atom[0] == '"':
        if not is_proper_quote(atom):
            return "EOF"
        return '"' + escape(atom[1:-1]) + '"'
    if is_integer(atom):
        return int(atom)
    if atom in special_chars:
        reader.next()
        res_lst = mal_types.MalList("(")
        res_lst.append(special_chars[atom])
        res_lst.append(read_form(reader))
        return res_lst
    if atom == "^":
        res_lst = mal_types.MalList("(")
        res_lst.append("with-meta")
        reader.next()
        second = read_form(reader)
        reader.next()
        first = read_form(reader)
        res_lst.append(first)
        res_lst.append(second)
        return res_lst
    if atom == "true":
        return True
    if atom == "false":
        return False
    if atom == "nil":
        return None
    else:
        return atom

def is_proper_quote(string):
    if re.match(r'"(?:\\.|[^\\"])*"', string):
        return True
    return False

def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False
