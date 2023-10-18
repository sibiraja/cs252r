# THIS BUSTLE IMPLEMENTATION IS FOR THE ARITHMETIC DSL. TODO: ONCE I GET STRING BUSTLE TO WORK (IN ANOTHER FILE), I CAN THEN COMBINE THEM INTO ONE FILE CALLED BUSTLEALGO
# AND DEFINE MY EXAMPLES AND OPERATORS IN ANOTHER FILE  

import itertools
from tqdm import tqdm

# List of tasks, where each task is a list of IO examples.
arithmetic_input_output_examples = [
    # [([1,2], 3), ([2,3], 5), ([3,4], 7), ([4,5], 9)], # add 2 numbers
    [([1,2], 2), ([2,3], 6), ([3,4], 12), ([4,5], 20)], # multiply 2 numbers
    # [([1,2], -1), ([2,3], -1), ([3,4], -1), ([4,6], -2)], # subtract 2 numbers
    # [([1,2], 0), ([6,3], 2), ([10,4], 2), ([49,7], 7)], # divide 2 numbers
    # [([1,3], 8), ([2,4], 12), ([3,7], 20), ([4,8], 24)], # add 2 numbers and multiply result by 2
    # [([1,3], 13), ([2,5], 25), ([3,7], 37), ([4,3], 23)], # add 2 numbers, multiply result by 4, and subtract 3 --> this example takes up too much RAM???? Getting a leaked semaphore error lol

]

programs_found = []

operations = [("ADD", 2), ("MULTIPLY", 2), ("SUBTRACT", 2), ("DIVIDE", 2)]

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

    for k, v in input_mapping.items():
        expr = expr.replace(k, str(v))

    if input_mapping == {}:
        return expr

    try:
        temp = str(eval(expr))
    except ZeroDivisionError: # TODO: CAN ALSO ADD OTHER ERROR CHECKS HERE RELEVEANT TO STRING DSL MAYBE?
        return "ERROR"
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
                curr_results = tuple(curr_results)
                results_seen.add(curr_results)
    E[1].extend([("VAR", f"x{i}") for i in range(len(task_examples[0][0]))])  # Add the input variables


    args_to_weights = {}
    for weight, expressions in E.items():
        for expr in expressions:
            args_to_weights[expr] = weight

    # Add numerical constants to E
    for i in range(1, 10):
        if ("CONST", str(i)) not in E[1]:
            E[1].append(("CONST", str(i)))
            args_to_weights[("CONST", str(i))] = 1
            curr_results = [str(i)] * len(task_examples)
            curr_results = tuple(curr_results)
            results_seen.add(curr_results)

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
                    args_to_execute.append(evaluate_expression(arg[1], {}))


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

                if len(programs_found) == len(arithmetic_input_output_examples):
                    print("=====================================")
                    print("WE HAVE FOUND THE FOLLOWING PROGRAMS: ")
                    for program in programs_found:
                        print(program)
                    print("DONE")
                    exit()

print("If we reached this point, we did not synthesize programs :(")