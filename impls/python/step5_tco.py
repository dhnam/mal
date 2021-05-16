import reader
import printer
from mal_types import MalList
from env import Env, NotFoundException
from core import ns

repl_env = Env(None)
for key, value in ns.items():
    repl_env.set_(key, value)

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
    while 1:
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
            env = let_env
            ast = ast[2]
            continue
        if ast[0] == "do":
            for next_ast in ast[1:-1]:
                final = eval_(next_ast, env)
            ast = ast[-1]
            continue
        if ast[0] == "if":
            cond = eval_(ast[1], env)
            if cond == 0 and type(cond) == int:
                cond = True # Counting number 0 as True
            if cond is None:
                cond = False
            if cond != False:
                ast = ast[2]
                continue
            if cond == False and len(ast) <= 3:
                return None
            ast = ast[3]
            continue
        if ast[0] == "fn*":
            def closure(binds, exprs, *args):
                fn_env = Env(env, binds=binds, exprs=args)
                return eval_(exprs, fn_env)
            return {
                    "ast": ast[2],
                    "params": ast[1],
                    "env": env,
                    "fn": lambda *x: closure(ast[1], ast[2], *x),
                    }
        else:
            eval_list = eval_ast(ast, env)
            if type(eval_list[0]) == dict:
                f = eval_list[0]
                ast = f["ast"]
                env = Env(outer=f["env"], binds=f["params"], exprs=eval_list[1:])
                continue
            else:
                return eval_list[0](*eval_list[1:])


def print_(print_arr):
    return printer.pr_str(print_arr)

def rep(read_str):
    try:
        ast = read_(read_str)
    except EOFError:
        return "EOF"
    try:
        print_arr = eval_(ast, repl_env)
    except NotFoundException as e:
        return "'" + str(e) + "'" + " not found."
    return print_(print_arr)

def main():
    rep("(def! not (fn* (a) (if a false true)))")
    while 1:
        try:
            read_str = input("user> ")
        except EOFError:
            break
        print(rep(read_str))

if __name__ == "__main__":
    main()
