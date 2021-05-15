import reader
import mal_types

def revert_escape(string):
    return string.replace('\\', r'\\').replace('\n', r'\n').replace('\"', r'\"')

def pr_str(data, print_readably=True):
    if type(data) == mal_types.MalList:
        closer = data.closer
        opener = data.opener
        data_str =  " ".join([pr_str(x, print_readably) for x in data])
        data_str = opener + data_str + closer
        return data_str
    else:
        return pr_str_nonlist(data, print_readably) 

def pr_str_nonlist(data, print_readably):
    if type(data) == int:
        return str(data)
    if type(data) == str and data[0] == '"':
        if print_readably:
            data = '"' + revert_escape(data[1:-1]) + '"'
            return data
        return data[1:-1]
    if data == True:
        return "true"
    if data == False:
        return "false"
    if data is None:
        return "nil"
    if type(data) == type(lambda x:None):
        return "#<function>"
    return data
