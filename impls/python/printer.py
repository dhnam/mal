import reader

def pr_str(data):
    if type(data) == list:
        opener = data[0]
        try:
            closer = reader.bracket_pair[opener]
            del data[0]
        except KeyError:
            opener = "("
            closer = ")"
        data_str =  " ".join(map(pr_str, data))
        data_str = opener + data_str + closer
        return data_str
    else:
        return pr_str_nonlist(data) 

def pr_str_nonlist(data):
    if type(data) == int:
        return str(data)
    if type(data) == str:
        return data
    else:
        return data
