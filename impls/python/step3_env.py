import reader
import printer
from mal_types import MalList
from env import Env, NotFoundException

repl_env = Env(None)
repl_env.set_("+", lambda a,b: a+b)
repl_env.set_("-", lambda a,b: a-b)
repl_env.set_("*", lambda a,b: a*b)
repl_env.set_("/", lambda a,b: a//b)

def read_(read_str):
    return reader.read_str(read_str)

def eval_ast(ast, env: Env):
    if type(ast) == str and ast[0] not in ':"': 
        return env.get(ast) # It raises error
    if type(ast) == str and ast[0] in '":':
        return ast
    if type(ast) == MalList:
        res = MalList(ast.opener)
        res += [eval_(x, env) for x in ast]
        return res
    return ast

def eval_(ast, env: Env):
    if type(ast) != MalList or ast.opener != "(":
        return eval_ast(ast, env)
    if len(ast) == 0:
        return ast
    if ast[0] == "def!":
        second_param = eval_(ast[2], env)
        env.set_(ast[1], second_param)
        return second_param
    if ast[0] == "let*":
        let_env = Env(env)
        bindings = ast[1]
        i = 0
        while 1:
            try:
                let_env.set_(bindings[i], eval_(bindings[i + 1], let_env))
                i += 2
            except IndexError:
                break
        return eval_(ast[2], let_env)
    else:
        eval_list = eval_ast(ast, env)
        return eval_list[0](*eval_list[1:])

def print_(print_arr):
    return printer.pr_str(print_arr)

def rep(read_str):
    ast = read_(read_str)
    try:
        print_arr = eval_(ast, repl_env)
    except NotFoundException as e:
        return "'" + str(e) + "'" + " not found."
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
