import reader
import printer
from mal_types import MalList, MalException
from env import Env, NotFoundException
from core import ns

repl_env = Env(None)
for key, value in ns.items():
    repl_env.set_(key, value)
repl_env.set_("eval", lambda x: eval_(x, repl_env))

#monkey_patch function
def is_macro(func):
    try:
        if type(func) == dict:
            return func["is_macro"]
        return func.is_macro
    except AttributeError:
        return False
    except KeyError:
        return False

def is_macro_call(ast, env:Env):
    if type(ast) == MalList and ast.opener == "(" and len(ast) > 0 and type(ast[0]) == str:
        try:
            is_macro_func = is_macro(env.get(ast[0]))
        except NotFoundException:
            return False
        return is_macro_func
    return False

def macroexpand(ast, env:Env):
    while is_macro_call(ast, env):
        symbol = env.get(ast[0])
        if type(symbol) == dict:
            ast = symbol["fn"](*ast[1:])
        else:
            ast = symbol(*ast[1:])
    return ast

            
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
        ast = macroexpand(ast, env)
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
            do_ast = MalList("(")
            do_ast += ast[1:-1]
            eval_ast(do_ast, env)
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
        if ast[0] == "quote":
            return ast[1]
        if ast[0] == "quasiquote" or ast[0] == "quasiquoteexpand":
            def quasiquote(param):
                def in_list(param):
                    res = MalList("(")
                    for elt in reversed(param):
                        if type(elt) == MalList and len(elt) > 1 and elt[0] == "splice-unquote":
                            tmp = MalList("(")
                            tmp.append("concat")
                            tmp.append(elt[1])
                            tmp.append(res)
                            res = tmp
                        else:
                            tmp = MalList("(")
                            tmp.append("cons")
                            tmp.append(quasiquote(elt))
                            tmp.append(res)
                            res = tmp
                    return res
                if type(param) == MalList and param.opener == "(" and len(param) > 0 and param[0] == "unquote":
                    return param[1]
                elif type(param) == MalList and param.opener == "(":
                    return in_list(param)
                elif (type(param) == MalList and param.opener == "{") or (type(param) == str):
                    tmp = MalList("(")
                    tmp.append("quote")
                    tmp.append(param)
                    return tmp
                elif type(param) == MalList and param.opener == "[":
                    tmp = MalList("(")
                    tmp.append("vec")
                    tmp.append(in_list(param))
                    return tmp
                else:
                    return param

            if ast[0] == "quasiquote":
                ast = quasiquote(ast[1])
                continue
            else:
                return quasiquote(ast[1])

        if ast[0] == "defmacro!":
            second_param = eval_(ast[2], env)
            if type(second_param) != dict:
                second_param.is_macro = True 
            else:
                second_param["is_macro"] = True
            env.set_(ast[1], second_param)
            return second_param
        if ast[0] == "macroexpand":
            return macroexpand(ast[1], env)
        if ast[0] == "try*":
            try:
                return eval_(ast[1], env)
            except MalException as e:
                if len(ast) > 2 and ast[2][0] == "catch*":
                    env = Env(outer=env, binds=[ast[2][1]], exprs=[e.args[0]])
                    ast = ast[2][2]
                    continue
                else:
                    raise e
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
    except reader.NoTokenException:
        return ""
    try:
        print_arr = eval_(ast, repl_env)
    except NotFoundException as e:
        return str(e)
    except IndexError:
        return ast
    except MalException as e:
        return "Exception " + printer.pr_str(e.args[0])
    return print_(print_arr)

import sys

def main():
    rep("(def! not (fn* (a) (if a false true)))")
    rep("(def! load-file (fn* (f) (eval (read-string (str \"(do \" (slurp f) \"\\nnil)\")))))")
    rep("(defmacro! cond (fn* (& xs) (if (> (count xs) 0) (list 'if (first xs) (if (> (count xs) 1) (nth xs 1) (throw \"odd number of forms to cond\")) (cons 'cond (rest (rest xs)))))))")
    argv_lst = MalList("(")
    argv_lst += ['"' + reader.read_str(x) + '"' for x in sys.argv[2:]]
    repl_env.set_("*ARGV*", argv_lst)
    if len(sys.argv) > 1:
        rep("(load-file \"" + sys.argv[1] + '")')
        return
    while 1:
        try:
            read_str = input("user> ")
        except EOFError:
            break
        print(rep(read_str))

if __name__ == "__main__":
    main()
