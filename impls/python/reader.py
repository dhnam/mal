import re
# TODO put 'quote' or such in list with following element

bracket_pair = {
        "(": ")",
        "[": "]",
        "{": "}",
        }
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
    res = []
    res.append(opener)
    closer = bracket_pair[opener]
    try:
        for i in reader:
            next_atom = read_form(reader)
            if next_atom == closer:
                break
            res.append(next_atom)
    except IndexError:
        return "EOF"
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
    if atom.isdecimal():
        return int(atom)
    if atom in special_chars:
        reader.next()
        return [special_chars[atom], read_form(reader)]
    if atom == "^":
        reader.next()
        second = read_form(reader)
        reader.next()
        first = read_form(reader)
        return ["with-meta", first, second]
    else:
        return atom

def is_proper_quote(string):
    if re.match(r'"(?:\\.|[^\\"])*"', string):
        return True
    return False

