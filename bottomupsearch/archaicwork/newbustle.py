import itertools
from tqdm import tqdm

# List of tasks, where each task is a list of IO examples.
arithmetic_input_output_examples = [
    # [([1,2], 3), ([2,3], 5), ([3,4], 7), ([4,5], 9)], # add 2 numbers
    # [([1,2], 2), ([2,3], 6), ([3,4], 12), ([4,5], 20)], # multiply 2 numbers
    # [([1,2], -1), ([2,3], -1), ([3,4], -1), ([4,6], -2)], # subtract 2 numbers
    # [([1,2], 0), ([6,3], 2), ([10,4], 2), ([49,7], 7)], # divide 2 numbers
    # [([1,3], 8), ([2,4], 12), ([3,7], 20), ([4,8], 24)], # add 2 numbers and multiply result by 2
    [([1,3], 13), ([2,5], 25), ([3,7], 37), ([4,3], 23)], # add 2 numbers, multiply result by 4, and subtract 3 --> this example takes up too much RAM???? Getting a leaked semaphore error lol

]

programs_found = []

# operations = ["ADD", "SUBTRACT", "MULTIPLY", "DIVIDE"]
operations = [("ADD", 2), ("MULTIPLY", 2), ("SUBTRACT", 2), ("DIVIDE", 2)]
# operations = [("ADD", 2), ("MULTIPLY", 2)]

# def execute(op, *args):
#     if op == "ADD":
#         return args[0] + args[1]
#     elif op == "MULTIPLY":
#         return args[0] * args[1]
#     elif op == "VAR":
#         return args[0]

def get_expression(op, *args):
    if op == "ADD":
        return f"({args[0]} + {args[1]})"
    elif op == "MULTIPLY":
        return f"({args[0]} * {args[1]})"
    elif op == "SUBTRACT":
        return f"({args[0]} - {args[1]})"
    elif op == "DIVIDE":
        return f"({args[0]} // {args[1]})"
    # elif op == "VAR":
    #     return f"{args[0]}"

def evaluate_expression(expr, input_mapping):
    # print("=====================================")
    # print("INPUT MAPPING: ", input_mapping)

    # print("EXPRESSION BEFORE REPLACEMENT: ", expr)
    for k, v in input_mapping.items():
        expr = expr.replace(k, str(v))
    # print("EXPRESSION AFTER REPLACEMENT: ", expr)

    if input_mapping == {}:
        # print("NO INPUT MAPPING, SO EXPRESSION IS ALREADY EVALUATED")
        return expr

    try:
        temp = str(eval(expr))
    except ZeroDivisionError: # TODO: CAN ALSO ADD OTHER ERROR CHECKS HERE RELEVEANT TO STRING DSL MAYBE?
        # print("ZERO DIVISION ERROR")
        return "ERROR"
    
    # print("EVALUATED EXPRESSION: ", temp)
    return temp

max_weight = 7 # this represents the actual term weight for our desired expression

# Now, for each task's examples, run the synthesis process.
for task_examples in arithmetic_input_output_examples:

    E = {1: []}
    results_seen = set()

    for io_example in task_examples:
        for element in io_example[0]:
            element = str(element)
            if ("CONST", element) not in E[1]:
                E[1].append(("CONST", element))
                curr_results = [str(element)] * len(task_examples)
                curr_results = tuple(curr_results) # convert the list to a tuple since sets cannot contain lists
                results_seen.add(curr_results)
    E[1].extend([("VAR", f"x{i}") for i in range(len(task_examples[0][0]))])  # Add the input variables
    # variable_set = set([f"x{i}" for i in range(len(task_examples[0][0]))])


    # print(f"\nE: {E}\n")

    args_to_weights = {}
    for weight, expressions in E.items():
        for expr in expressions:
            args_to_weights[expr] = weight

    for i in range(1, 10):
        if ("CONST", str(i)) not in E[1]:
            E[1].append(("CONST", str(i)))
            args_to_weights[("CONST", str(i))] = 1
            curr_results = [str(i)] * len(task_examples)
            curr_results = tuple(curr_results)
            results_seen.add(curr_results)

    # print(results_seen)
    # exit()

    # print(f"args_to_weights: {args_to_weights}\n")
    # exit()

    # for w in range(2, max_weight + 1):
    for w in tqdm(range(2, max_weight + 1)):
        # print("W is now: ", w)
        for operation_tuple in operations:
            # print("We are now considering the following operation: ", operation_tuple)

            operation = operation_tuple[0]

            n_op_arity = operation_tuple[1] # plug 

            A = []
            values_in_E = [item for sublist in E.values() for item in sublist]
            # print(f"values_in_E: {values_in_E}")
            # exit()
            # values_in_E = [item for sublist in E.values() for item in sublist] + [("CONST", i) for i in range(1, 6)]
            # values_in_E = list(set([item for sublist in E.values() for item in sublist] + [("CONST", i) for i in range(1, 6)]))


            permutations = list(itertools.permutations(values_in_E, n_op_arity))
            # print(f"permutations: {permutations}")

            for permutation in permutations:
                for arg in permutation:
                    if arg not in args_to_weights:
                        print("WEIGHT NOT FOUND")
                sum_of_weights = sum([args_to_weights[arg] for arg in permutation])
                # print("Current permutation: ", permutation, " has weight: ", sum_of_weights, " and we are looking for weight: ", w)
                if sum_of_weights == w - 1:
                    A.append(permutation)

            # print(f"\nWeight: {w}")
            # print(f"Possible combinations (A): {A}\n")
            # exit()

            # print("A: " , A)

            for arg_tuple in A:
                # print("Hi!")

                # consider the case where we have already found a program satisfying the current task via an expression constructed from a previous arg_tuple.
                # Then we want to break out of this loop and continue to the next task
                answer_needed = []
                for (input_values, output) in task_examples:
                    answer_needed.append(output)
                
                if tuple(answer_needed) in results_seen:
                    # print("Hello")
                    break


                # print(f"arg_tuple: {arg_tuple}")
                # exit()
                # result = execute(operation, *(arg[1] for arg in arg_tuple))
                # args_to_execute = [evaluate_expression(arg[1], {}) if arg[0] == "EXPR" else arg[1] for arg in arg_tuple]
                # args_to_execute = [arg[1] if arg[0] == "CONST" else evaluate_expression(arg[1], {}) for arg in arg_tuple]
                
                # args_to_execute = [arg[1] if arg[0] == "CONST" else evaluate_expression(arg[1], {}) for arg in arg_tuple]
                args_to_execute = []
                for arg in arg_tuple:
                    args_to_execute.append(evaluate_expression(arg[1], {}))

                # print("ARGS TO EXECUTE ON: ", args_to_execute)
                # exit()

                    # if arg[0] == "CONST":
                    #     args_to_execute.append(arg[1])
                    # elif arg[0] == "VAR":
                    #     args_to_execute.append(arg[1])
                    # else:



                        # args_to_execute.append(evaluate_expression(arg[1], {}))

                        # # if there are no variables in the expression, then evaluate it
                        # if "x" not in arg[1]:
                        #     args_to_execute.append(evaluate_expression(arg[1], {}))
                        # else:
                        #     args_to_execute.append(evaluate_expression(arg[1], {}))

                        
                        # try to evaluate the expression. Catch a type



                # for weight, expressions in E.items():
                #     for expr in expressions:
                #         if expr[0] == "VAR":
                #             args_to_weights[expr] = 1  # Assigning weight of 1 to variables
                #         else:
                #             args_to_weights[expr] = weight


                # print(f"args_to_execute: {args_to_execute}")


                expr = get_expression(operation, *(args_to_execute))
                # print("EXPR: ", expr)

                # TODO: ADD THE NEW EXPRESSIONS TO THE MAPPING E AND THE MAPPING args_to_weights if the weight is not already in E
                # but only add the expression if it consists of only constants and variables
                # expr_split = expr.split()

                # add_to_E = True
                # for i in range(1, len(expr)):
                #     letter = expr[i]
                #     if letter.isdigit() and (expr[i-1].isdigit()):
                #         add_to_E = False
                #         break
                # for i, letter in enumerate(expr):
                #     if letter.isdigit() and (i == 0 or expr[i - 1] != "x"): # this assume we will not have more than 9 variables. I think this is fair assumption as that will be take too long to search for and synthesize a program anyways
                #         add_to_E = False
                #         print("Hello")
                #         break
                # if add_to_E:
                #     if w not in E:
                #         E[w] = [("EXPR", expr)]
                #         args_to_weights[("EXPR", expr)] = w

                #         print("JUST ADDED: ", expr, "with weight: ", w, "\n")

                # if expr == "((x0 + x1) + 1)":
                #     if expr in 
                # for element in expr_split:


                # print("EXPR: ", expr)
                # if expr == "(x0 + x1)":
                #     print("FOUND IT")
                    # exit()


                # Keep a list of what the current expression evaluates to for each example in the task.
                curr_results = []


                all_correct = True
                for (input_values, output) in task_examples:
                    input_mapping = {f"x{i}": v for i, v in enumerate(input_values)}
                    # print("=====================================")
                    # print("INPUT MAPPING: ", input_mapping)


                    expr_result = evaluate_expression(expr, input_mapping)
                    # if expr == "((x0 + x1) + 1)":
                    #     print("Evaluting expression: ", expr, "with input mapping: ", input_mapping, "and result: ", expr_result)
                    
                    if expr_result == "ERROR":
                        all_correct = False
                        break

                    curr_results.append(expr_result)

                    if expr_result != str(output):
                        # if expr == "(x0 + x1)":
                        #     print("Something went wrong")
                        #     exit()
                        all_correct = False
                        # break --> don't break here, because we want to add the expression to E even if it is incorrect for some examples in order to correctly get all the results of an expression before checking if we need to add it to E

                # print(f"THE CURRENT EXPRESSION {expr} HAD THE FOLLOWING RESULTS: ", curr_results, "for task: ", task_examples, "with weight: ", w, "\n")
                # exit()

                

                
                if len(curr_results) == len(task_examples):
                    # print("Hello")
                    if tuple(curr_results) not in results_seen:
                        results_seen.add(tuple(curr_results))

                        if w not in E:
                            E[w] = []
                        
                        E[w].append(("EXPR", expr))
                        args_to_weights[("EXPR", expr)] = w

                        # print("JUST ADDED THE SUBEXPRESSION: ", expr, "with weight: ", w, "\n")
                    
                    else:
                        # print("WE HAVE ALREADY ACHIEVED THESE SETS OF RESULTS VIA ANOTHER EXPRESSION \n")
                        all_correct = False # set this to false to indicate that we shouldn't add this program to our global bank


                # only add a program to our global answer bank if it is the first program to satisfy the input output examples. otherwise, continue searching for the next program
                # --> we take care of this at the top of loop

                # only consider adding the current expression if it has the correct number of results in curr_results (otherwise it errored out on at least 1 example, so its invalid) and if all results are correct
                if all_correct and len(curr_results) == len(task_examples):
                    # print(f"Found a program that fits the task: {expr}")
                    # print("This program works: ", expr, "for task: ", task_examples, "with weight: ", w, "\n")
                    programs_found.append("This program works: " + expr + "for task: " + str(task_examples) + "with weight: " + str(w) + "\n")

                if len(programs_found) == len(arithmetic_input_output_examples):
                    print("=====================================")
                    print("WE HAVE FOUND THE FOLLOWING PROGRAMS: ")
                    for program in programs_found:
                        print(program)
                    print("DONE")
                    exit()

                # if expr == "(x0 + x1)":
                #     print("Something went wrong")

print("If we reached this point, we did not synthesize programs :(")





                # try:
                #     result = execute(operation, *args_to_execute)
                # except ZeroDivisionError:
                #     continue
                # expr = get_expression(operation, *(str(arg[1]) for arg in arg_tuple))

                # # Check if the resulting expression hasn't been added yet.
                # if ("EXPR", expr) not in [item for sublist in E.values() for item in sublist]:
                #     if w not in E:
                #         E[w] = []
                #     E[w].append(("EXPR", expr))
                #     args_to_weights[("EXPR", expr)] = w  # Update args_to_weights

                # # print("EXPR: ", expr)

                # # Check if the resulting expression is correct for all examples of the current task.
                # all_correct = True
                # print("TASK EXAMPLES: ", task_examples)
                # for (input_values, output) in task_examples:
                #     print("=====================================")
                #     print("INPUT VALUES: ", input_values, "; OUTPUT: ", output)
                #     input_mapping = {f"x{i}": v for i, v in enumerate(input_values)}
                #     # print(f"input_mapping: {input_mapping}")
                #     if evaluate_expression(expr, input_mapping) != output:
                #         all_correct = False
                #         break
                # if all_correct:
                #     print(f"Found a program that fits the task: {expr}")
                #     break
