# STRING DSL

import itertools
from tqdm import tqdm

# List of tasks, where each task is a list of IO examples.
string_input_output_examples = [
    [(["hello"], "h"), (["world"], "w"), (["goodbye"], "g"), (["bye"], "b")], # get left most character
    [(["hello"], "o"), (["world"], "d"), (["goodbye"], "e"), (["bye"], "e")], # get right most character

]

programs_found = []

# operations = [("LEFT", 1), ("RIGHT", 1), ("CONCATENATE", 2)]
operations = [("LEFT", 1), ("RIGHT", 1)]

def get_expression(op, *args):
    if op == "LEFT":
        temp = f"'{args[0]}'[0]"
        print("GOT THE LEFT OPERATION AND THE ARGUMENT IS: ", args[0], " AND THE RESULT IS: ", temp)
        return temp
    elif op == "RIGHT":
        temp = f"'{args[0]}'[-1]"
        print("GOT THE RIGHT OPERATION AND THE ARGUMENT IS: ", args[0], " AND THE RESULT IS: ", temp)
        return temp
    # elif op == "RIGHT":
    #     return f"({args[0]}[-1])"
    # elif op == "CONCATENATE":
    #     return f"({args[0]} + {args[1]})"

def evaluate_expression(expr, input_mapping):

    print("Evaluating expression: ", expr)

    for k, v in input_mapping.items():
        expr = expr.replace(k, str(v))

    if input_mapping == {}:
        print("INPUT MAPPING IS EMPTY, SO SUCCESSFULLY EVALUTED EXPRESSION: ", expr, " RESULT WAS: ", expr)
        return expr

    try:
        temp = str(eval(expr))
    except ZeroDivisionError: # TODO: CAN ALSO ADD OTHER ERROR CHECKS HERE RELEVEANT TO STRING DSL MAYBE?
        print("GOT AN ERROR")
        return "ERROR"

    print("SUCCESSFULLY EVALUTED EXPRESSION: ", expr, " RESULT WAS: ", temp)
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

    # # Add numerical constants to E --> can add this back later to allow for LEFT 1, LEFT 2, etc. rather than only leftmost character (which is LEFT 1)
    # for i in range(1, 10):
    #     if ("CONST", str(i)) not in E[1]:
    #         E[1].append(("CONST", str(i)))
    #         args_to_weights[("CONST", str(i))] = 1
    #         curr_results = [str(i)] * len(task_examples)
    #         curr_results = tuple(curr_results)
    #         results_seen.add(curr_results)

    # add space character to E
    if ("CONST", " ") not in E[1]:
        E[1].append(("CONST", " "))
        args_to_weights[("CONST", " ")] = 1
        curr_results = [" "] * len(task_examples)
        curr_results = tuple(curr_results)
        results_seen.add(curr_results)

    print("E: ", E)
    print("args_to_weights: ", args_to_weights)
    

    # for w in range(2, max_weight + 1):
    for w in tqdm(range(2, max_weight + 1)):
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

            print("A: ", A)

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
                    args_to_execute.append(evaluate_expression(arg[1], {})) # in a math expression, representing subexpressions as tuples means they will have parenthesis around them (which is fine and needed) --> we can't do this with strings.


                expr = get_expression(operation, *(args_to_execute))

                # Keep a list of what the current expression evaluates to for each example in the task.
                curr_results = []


                all_correct = True
                for (input_values, output) in task_examples:
                    input_mapping = {f"x{i}": v for i, v in enumerate(input_values)}



                    expr_result = evaluate_expression(expr, input_mapping)
                    
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

                if len(programs_found) == len(string_input_output_examples):
                    print("=====================================")
                    print("WE HAVE FOUND THE FOLLOWING PROGRAMS: ")
                    for program in programs_found:
                        print(program)
                    print("DONE")
                    exit()

print("If we reached this point, we did not synthesize programs :(")