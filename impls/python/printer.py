import reader
import mal_types

def pr_str(data):
    if type(data) == mal_types.MalList:
        closer = data.closer
        opener = data.opener
        data_str =  " ".join([pr_str(x) for x in data])
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
