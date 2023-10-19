def test():
    print("Hello from helper.py")

def retrieve_arithmetic_io_examples():

    arithmetic_input_output_examples = [
        [([1,2], 3), ([2,3], 5), ([3,4], 7), ([4,5], 9)], # add 2 numbers
        [([1,2], 2), ([2,3], 6), ([3,4], 12), ([4,5], 20)], # multiply 2 numbers
        [([1,2], -1), ([2,3], -1), ([3,4], -1), ([4,6], -2)], # subtract 2 numbers
        [([1,2], 0), ([6,3], 2), ([10,4], 2), ([49,7], 7)], # divide 2 numbers
        # [([1,3], 8), ([2,4], 12), ([3,7], 20), ([4,8], 24)], # add 2 numbers and multiply result by 2
    ]

    return arithmetic_input_output_examples

def retrieve_string_io_examples():
    string_input_output_examples = [
        [(["he", "llo"], "l"), (["w", "orld"], "r"), (["good", "bye"], "o"), (["tes", "ting"], "s")], # concat then get 3 character from the leftmost
        [(["he", "llo"], "hello"), (["w", "orld"], "world"), (["goodb", "ye"], "goodbye"), (["bye", ""], "bye")], # concatenate
        [(["hello"], "h"), (["world"], "w"), (["goodbye"], "g"), (["bye"], "b")], # get left most character
        [(["hello"], "o"), (["world"], "d"), (["goodbye"], "e"), (["bye"], "e")], # get right most character
        [(["hello"], "e"), (["world"], "o"), (["goodbye"], "o"), (["bye"], "y")], # get 2nd character
        [(["hello"], "l"), (["world"], "l"), (["goodbye"], "y"), (["bye"], "y")], # get 2nd to last character
        
    ]

    return string_input_output_examples

def retrieve_io_examples(domain):
    if domain == "arithmetic":
        return retrieve_arithmetic_io_examples()
    elif domain == "string":
        return retrieve_string_io_examples()


def retrieve_arithmetic_operations():
    arithmetic_operations = [("ADD", 2), ("MULTIPLY", 2), ("SUBTRACT", 2), ("DIVIDE", 2)]
    return arithmetic_operations

def retrieve_string_operations():
    string_operations = [("Left", 2), ("Right", 2), ("Concatenate", 2)]
    return string_operations


def retrieve_operations(domain):
    if domain == "arithmetic":
        return retrieve_arithmetic_operations()
    elif domain == "string":
        return retrieve_string_operations()


def arithmetic_get_expression(op, args):
    if op == "ADD":
        return f"({args[0]} + {args[1]})"
    elif op == "MULTIPLY":
        return f"({args[0]} * {args[1]})"
    elif op == "SUBTRACT":
        return f"({args[0]} - {args[1]})"
    elif op == "DIVIDE":
        return f"({args[0]} // {args[1]})"

def string_get_expression(op, args):

    if op == "Left":

        # error check for wrong arg types here. if wrong data types, return "ERROR"
        if type(args[0]) != str or type(args[1]) != int: # or args[1] < 0 or args[1] > 9 or args[1] >= len(args[0])
            return "ERROR"

        if args[1] >= 0:
            if args[1] >= len(args[0]):
                return "ERROR"

        temp = f"'{args[0]}'[{args[1]}]"
        return temp
    
    elif op == "Right":

        # error check for wrong arg types here. if wrong data types, return "ERROR"
        if type(args[0]) != str or type(args[1]) != int: # or args[1] < 0 or args[1] > 9 or args[1] >= len(args[0])
            return "ERROR"

        if args[1] > len(args[0]): # use greater than here since indexing from the right starts at 1
                return "ERROR"

        temp = f"'{args[0]}'[-{args[1]}]"
        return temp

    elif op == "Concatenate":

        # error check for wrong arg types here. if wrong data types, return "ERROR"
        if type(args[0]) != str or type(args[1]) != str:
            return "ERROR"

        temp = f"'{args[0]}'+'{args[1]}'"
        return temp


def string_get_eval(expr, input_mapping):

    if type(expr) == int:
        return expr

    for k, v in input_mapping.items():
        expr = expr.replace(k, str(v))

    if input_mapping == {}:
        if "[" in expr or "+" in expr:
            ans = str(eval(expr))
            return ans
        ans = expr
        return ans

    try:
        temp = str(eval(expr))
    except IndexError:
        return "ERROR"
    return temp

def arithmetic_get_eval(expr, input_mapping):
    for k, v in input_mapping.items():
        expr = expr.replace(k, str(v))

    if input_mapping == {}:
        return expr

    try:
        temp = str(eval(expr))
    except ZeroDivisionError:
        return "ERROR"
    return temp