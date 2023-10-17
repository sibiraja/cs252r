import itertools
from tqdm import tqdm

# List of tasks, where each task is a list of IO examples.
arithmetic_input_output_examples = [
    [([1,2], 3), ([2,3], 5), ([3,4], 7), ([4,5], 9)], # add 2 numbers
    [([1,2], 2), ([2,3], 6), ([3,4], 12), ([4,5], 20)], # multiply 2 numbers
    [([1,2], -1), ([2,3], -1), ([3,4], -1), ([4,6], -2)], # subtract 2 numbers
    [([1,2], 0), ([6,3], 2), ([10,4], 2), ([49,7], 7)], # divide 2 numbers
    # [([1,2], 1), ([2,3], 6), ([3,4], 8), ([4,5], 10)] # add 2 numbers and add 1 to result
]

# operations = ["ADD", "SUBTRACT", "MULTIPLY", "DIVIDE"]
operations = [("ADD", 2), ("MULTIPLY", 2), ("SUBTRACT", 2), ("DIVIDE", 2)]

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
    except ZeroDivisionError:
        print("ZERO DIVISION ERROR")
        return "ERROR"
    
    # print("EVALUATED EXPRESSION: ", temp)
    return temp

max_weight = 6

# Now, for each task's examples, run the synthesis process.
for task_examples in arithmetic_input_output_examples:

    E = {1: []}
    for io_example in task_examples:
        for element in io_example[0]:
            element = str(element)
            if ("CONST", element) not in E[1]:
                E[1].append(("CONST", element))
    E[1].extend([("VAR", f"x{i}") for i in range(len(task_examples[0][0]))])  # Add the input variables
    variable_set = set([f"x{i}" for i in range(len(task_examples[0][0]))])


    # print(f"\nE: {E}\n")

    args_to_weights = {}
    for weight, expressions in E.items():
        for expr in expressions:
            args_to_weights[expr] = weight

    # print(f"args_to_weights: {args_to_weights}\n")
    # exit()

    # for w in range(2, max_weight + 1):
    for w in tqdm(range(2, max_weight + 1)):
        for operation_tuple in operations:

            operation = operation_tuple[0]

            n_op_arity = operation_tuple[1]

            A = []
            values_in_E = [item for sublist in E.values() for item in sublist]
            # print(f"values_in_E: {values_in_E}")
            # exit()
            # values_in_E = [item for sublist in E.values() for item in sublist] + [("CONST", i) for i in range(1, 6)]
            # values_in_E = list(set([item for sublist in E.values() for item in sublist] + [("CONST", i) for i in range(1, 6)]))


            permutations = list(itertools.permutations(values_in_E, n_op_arity))
            # print(f"permutations: {permutations}")

            for permutation in permutations:
                sum_of_weights = sum([args_to_weights[arg] for arg in permutation])
                if sum_of_weights == w - 1:
                    A.append(permutation)

            # print(f"\nWeight: {w}")
            # print(f"Possible combinations (A): {A}\n")
            # exit()

            for arg_tuple in A:
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
                # if expr == "(x0 + x1)":
                #     print("FOUND IT")
                    # exit()


                all_correct = True
                for (input_values, output) in task_examples:
                    input_mapping = {f"x{i}": v for i, v in enumerate(input_values)}
                    # print("=====================================")
                    # print("INPUT MAPPING: ", input_mapping)


                    expr_result = evaluate_expression(expr, input_mapping)
                    
                    if expr_result == "ERROR":
                        all_correct = False
                        break

                    # TODO: ADD THE EVALUATED EXPRESSIONS TO THE MAPPING E AND THE MAPPING args_to_weights if the expression is not already in E

                    if expr_result != str(output):
                        # if expr == "(x0 + x1)":
                        #     print("Something went wrong")
                        #     exit()
                        all_correct = False
                        break
                
                if all_correct:
                    # print(f"Found a program that fits the task: {expr}")
                    print("This program works: ", expr, "for task: ", task_examples, "with weight: ", w, "\n")
                    # exit()

                # if expr == "(x0 + x1)":
                #     print("Something went wrong")

print("DONE")

# TODO: implement subtraction and integer division functionality
# TODO: handle zero division errors






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
