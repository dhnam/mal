import reader
import printer
from mal_types import MalList

repl_env = {
        "+": lambda a,b: a+b,
        "-": lambda a,b: a-b,
        "*": lambda a,b: a*b,
        "/": lambda a,b: a//b,
           }

def read_(read_str):
    return reader.read_str(read_str)

def eval_ast(ast, env):
    if type(ast) == str and ast[0] not in ':"': 
        return repl_env[ast] # It raises error
    if type(ast) == str and ast[0] in '":':
        return ast
    if type(ast) == MalList:
        res = MalList(ast.opener)
        res += [eval_(x, env) for x in ast]
        return res
    return ast

def eval_(ast, env):
    if type(ast) != MalList or ast.opener != "(":
        return eval_ast(ast, env)
    if len(ast) == 0:
        return ast
    eval_list = eval_ast(ast, env)
    return eval_list[0](*eval_list[1:])

def print_(print_arr):
    return printer.pr_str(print_arr)

def rep(read_str):
    ast = read_(read_str)
    try:
        print_arr = eval_(ast, repl_env)
    except KeyError:
        print_arr = []
    return print_(print_arr)

def main():
    while 1:
        try:
            read_str = input("user> ")
        except EOFError:
            break
        print(rep(read_str))

if __name__ == "__main__":
    main()
