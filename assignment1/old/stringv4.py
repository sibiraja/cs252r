# STRING DSL

import itertools
from tqdm import tqdm

# List of tasks, where each task is a list of IO examples.
string_input_output_examples = [
    # [(["hello"], "ho"), (["world"], "wd"), (["goodbye"], "ge"), (["bye"], "be")], # concatenate leftmost and rightmost characters
    # [(["he", "llo"], "l"), (["w", "orld"], "r"), (["good", "bye"], "o"), (["tes", "ting"], "s")], # concat then get 3 character from the leftmost
    [(["he", "llo"], "hello"), (["w", "orld"], "world"), (["goodb", "ye"], "goodbye"), (["bye", ""], "bye")], # concatenate
    # [(["hello"], "h"), (["world"], "w"), (["goodbye"], "g"), (["bye"], "b")], # get left most character
    # [(["hello"], "o"), (["world"], "d"), (["goodbye"], "e"), (["bye"], "e")], # get right most character
    # [(["hello"], "e"), (["world"], "o"), (["goodbye"], "o"), (["bye"], "y")], # get 2nd character
    # [(["hello"], "l"), (["world"], "l"), (["goodbye"], "y"), (["bye"], "y")], # get 2nd to last character

]

programs_found = []

# operations = [("Left", 2), ("Right", 2), ("Concatenate", 2)]
operations = [("Concatenate", 2)]

def get_expression(op, *args):

    if op == "Left":

        # error check for wrong arg types here. if wrong data types, return "ERROR"
        if type(args[0]) != str or type(args[1]) != int: # or args[1] < 0 or args[1] > 9 or args[1] >= len(args[0])
            return "ERROR"

        if args[1] >= 0:
            if args[1] >= len(args[0]):
                return "ERROR"

        temp = f'\'{args[0]}\'[{args[1]}]'
        print("GOT THE LEFT OPERATION AND THE ARGUMENT IS: ", args[0], " AND THE RESULT IS: ", temp)
        return temp
    
    elif op == "Right":

        # error check for wrong arg types here. if wrong data types, return "ERROR"
        if type(args[0]) != str or type(args[1]) != int: # or args[1] < 0 or args[1] > 9 or args[1] >= len(args[0])
            return "ERROR"

        if args[1] > len(args[0]): # use greater than here since indexing from the right starts at 1
                return "ERROR"

        # temp = f"'{args[0]}'[-{args[1]}]"
        temp = f'\'{args[0]}\'[-{args[1]}]'
        print("GOT THE RIGHT OPERATION AND THE ARGUMENT IS: ", args[0], " AND THE RESULT IS: ", temp)
        return temp

    elif op == "Concatenate":

        # error check for wrong arg types here. if wrong data types, return "ERROR"
        if type(args[0]) != str or type(args[1]) != str:
            return "ERROR"

        # temp = f"'{args[0]}'+'{args[1]}'"
        # temp = f'\'{args[0]}\'+\'{args[1]}\''
        temp = f'{args[0]}+{args[1]}'
        print("GOT THE CONCATENATE OPERATION AND THE ARGUMENTS ARE: ", args[0], " AND ", args[1], " AND THE RESULT IS: ", temp)
        return temp

def evaluate_expression(expr, input_mapping):

    if type(expr) == int:
        return expr

    print("Evaluating expression: ", expr)

    for k, v in input_mapping.items():
        expr = expr.replace(k, str(v))

    # if input_mapping == {}:
    #     print("INPUT MAPPING IS EMPTY")
    #     # if "[" in expr or "+" in expr:
    #         # print("testing....")
    #         # print("Before wrapping in quotes: ", expr)
    #         # expr = "\"" + expr + "\""
    #         # print("After wrapping in quotes: ", expr)
    #         # ans = str(eval(expr))
    #         # print("ANSWER IS: ", ans)
    #         # print("CYAAAA")
    #         # return ans
    #     ans = expr
    #     print("ANSWER IS: ", ans)
    #     return ans
        # expr = str(expr)

        # ex
        # try:
        #     temp = str(eval(expr))
        # except IndexError: # TODO: CAN ALSO ADD OTHER ERROR CHECKS HERE RELEVEANT TO STRING DSL MAYBE?
        #     print("GOT AN ERROR")
        #     return "ERROR"

        # print("SUCCESSFULLY EVALUTED EXPRESSION: ", expr, " RESULT WAS: ", temp)
        # return temp

    try:
        # temp = str(eval(expr))  --> # doesn't work ,need to wrap in double quotes
        # temp = str(eval(str(expr))) # doesn't work ,need to wrap in double quotes
        print("Original expr: ", expr)
        expr2 = ["\'", expr, "\'"]
        expr2 = "".join(expr2)
        print("New expr: ", expr2)
        # expr2 = "\" + expr + \""
        temp = str(eval(expr2))
    except IndexError: # TODO: CAN ALSO ADD OTHER ERROR CHECKS HERE RELEVEANT TO STRING DSL MAYBE?
        print("GOT AN ERROR")
        return "ERROR"

    print("SUCCESSFULLY EVALUTED EXPRESSION: ", expr2, " RESULT WAS: ", temp)
    return temp

max_weight = 3 # this represents the actual term weight for our desired expression

# Now, for each task's examples, run the synthesis process.
for task_examples in string_input_output_examples:

    E = {1: []}
    results_seen = set()

    for io_example in task_examples:
        for element in io_example[0]:
            # element = str(element)
            if ("CONST", element) not in E[1]:
                E[1].append(("CONST", element))
                curr_results = [element] * len(task_examples)
                curr_results = tuple(curr_results)
                results_seen.add(curr_results)
    E[1].extend([("VAR", f"x{i}") for i in range(len(task_examples[0][0]))])  # Add the input variables --> maybe edit this because right now it assumes the first IO example of each task is made up of the max args we will ever see in a task


    args_to_weights = {}
    for weight, expressions in E.items():
        for expr in expressions:
            args_to_weights[expr] = weight

    # Add numerical constants to E to allow LEFT and RIGHT to take in a number 0-9 that specifies which index to get
    for i in range(0, 10):
        if ("CONST", i) not in E[1]:
            E[1].append(("CONST", i))
            args_to_weights[("CONST", i)] = 1
            curr_results = [i] * len(task_examples)
            curr_results = tuple(curr_results)
            results_seen.add(curr_results)

    # add space character to E
    if ("CONST", " ") not in E[1]:
        E[1].append(("CONST", " "))
        args_to_weights[("CONST", " ")] = 1
        curr_results = [" "] * len(task_examples)
        curr_results = tuple(curr_results)
        results_seen.add(curr_results)
    # add empty string constant to E
    if ("CONST", "") not in E[1]:
        E[1].append(("CONST", ""))
        args_to_weights[("CONST", "")] = 1
        curr_results = [""] * len(task_examples)
        curr_results = tuple(curr_results)
        results_seen.add(curr_results)

    # print("E: ", E)
    # print("args_to_weights: ", args_to_weights)
    # exit()
    

    # for w in range(2, max_weight + 1):
    for w in tqdm(range(3, max_weight + 1)): # starting at 3 each operation takes 2 arguments, so an expression at minimum is of weight 3, but change back to 2 later (won't make a diff, just for easier debugging right now)
        # print("W is now: ", w)
        for operation_tuple in operations:

            operation = operation_tuple[0]

            n_op_arity = operation_tuple[1] # plug 

            A = []
            values_in_E = [item for sublist in E.values() for item in sublist]

            permutations = list(itertools.permutations(values_in_E, n_op_arity))

            for permutation in permutations:
                for arg in permutation:
                    if arg not in args_to_weights:
                        print("WEIGHT NOT FOUND")
                sum_of_weights = sum([args_to_weights[arg] for arg in permutation])
                if sum_of_weights == w - 1:
                    A.append(permutation)

            # print("A: ", A)

            for arg_tuple in A:

                # consider the case where we have already found a program satisfying the current task via an expression constructed from a previous arg_tuple.
                # Then we want to break out of this loop and continue to the next task
                answer_needed = []
                for (input_values, output) in task_examples:
                    answer_needed.append(output)
                
                if tuple(answer_needed) in results_seen:
                    # print("Hello")
                    break

                args_to_execute = []
                for arg in arg_tuple:
                    print("Current arg: ", arg)
                    args_to_execute.append(evaluate_expression(arg[1], {})) # in a math expression, representing subexpressions as tuples means they will have parenthesis around them (which is fine and needed) --> we can't do this with strings.


                print("args_to_execute: ", args_to_execute)


                expr = get_expression(operation, *(args_to_execute)) # add error checking for string DSL in this helper function since I can just continue to next arg_tuple if i have wrong data types as args
                if expr == "ERROR":
                    print("The expression ", expr, " is invalid, so we will continue to the next arg_tuple")
                    # exit()
                    continue
                else:
                    print("We constructed a valid expression: ", expr)
                    # exit()
                # print("expr: ", expr)
                # exit()

                # Keep a list of what the current expression evaluates to for each example in the task.
                curr_results = []


                all_correct = True
                for (input_values, output) in task_examples:
                    input_mapping = {f"x{i}": v for i, v in enumerate(input_values)}



                    expr_result = evaluate_expression(expr, input_mapping) # i did error checking in arithmetic domain in this helper function 
                    
                    if expr_result == "ERROR":
                        all_correct = False
                        break

                    curr_results.append(expr_result)

                    if expr_result != str(output):
                        all_correct = False
                

                
                if len(curr_results) == len(task_examples):
                    # print("Hello")
                    if tuple(curr_results) not in results_seen:
                        results_seen.add(tuple(curr_results))

                        if w not in E:
                            E[w] = []
                        
                        E[w].append(("EXPR", expr))
                        args_to_weights[("EXPR", expr)] = w


                    else:
                        all_correct = False # set this to false to indicate that we shouldn't add this program to our global bank


               
                # only consider adding the current expression if it has the correct number of results in curr_results (otherwise it errored out on at least 1 example, so its invalid) and if all results are correct
                if all_correct and len(curr_results) == len(task_examples):
                    programs_found.append("This program works: " + expr + "for task: " + str(task_examples) + "with weight: " + str(w) + "\n")
                    # programs_found.append("We used this operation: " + operation + " and these arguments: " + str(arg_tuple) + "\n")

                    # # format option 2: doesn't work for compound expressions
                    # temp_args = []
                    # temp_list = list(arg_tuple)
                    # for my_arg in temp_list:
                    #     temp_args.append(my_arg[1])
                    # temp_args = tuple(temp_args)
                    # programs_found.append(f"Solution: {operation}{temp_args}\n")

                if len(programs_found) == len(string_input_output_examples):
                    print("=====================================")
                    print("WE HAVE FOUND THE FOLLOWING PROGRAMS: ")
                    for program in programs_found:
                        print(program)
                    print("DONE")
                    exit()

print("If we reached this point, we did not synthesize programs :(")