def read_(read_str):
    return read_str

def eval_(input_str):
    return input_str

def print_(print_str):
    return print_str

def rep(read_str):
    input_str = read_(read_str)
    print_str = eval_(input_str)
    return print_(print_str)

def main():
    while 1:
        try:
            read_str = input("user> ")
        except EOFError:
            break
        print(rep(read_str))

if __name__ == "__main__":
    main()
