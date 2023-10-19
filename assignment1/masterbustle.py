import sys
import helper
import itertools
from tqdm import tqdm


# Bottom up synthesis algorithm
def main():
    domain = sys.argv[1]
    print(domain)
    if domain != "arithmetic" and domain != "string":
        raise ValueError("Invalid domain. Please enter 'arithmetic' or 'string'")
        exit()

    programs_found = []

    # Retrieve the input/output examples for the given domain
    input_output_examples = helper.retrieve_io_examples(domain)

    # Retrieve the operations for the given domain
    operations = helper.retrieve_operations(domain)

    if domain == "arithmetic":
        get_expression_function = helper.arithmetic_get_expression
        get_eval_function = helper.arithmetic_get_eval
        max_weight = 5 # This can go up to a max of 7 before it crashes an average laptop
    elif domain == "string":
        get_expression_function = helper.string_get_expression
        get_eval_function = helper.string_get_eval
        max_weight = 5 # 5 is the max for string DSL on an average laptop
    

    # Run BUS(tle) algorithm
    for task_examples in input_output_examples:

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

        

        # add domain-specific constants to E
        if domain == "arithmetic":
            for i in range(1, 10):
                if ("CONST", str(i)) not in E[1]:
                    E[1].append(("CONST", str(i)))
                    args_to_weights[("CONST", str(i))] = 1
                    curr_results = [str(i)] * len(task_examples)
                    curr_results = tuple(curr_results)
                    results_seen.add(curr_results)

        elif domain == "string":
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

        
        for w in tqdm(range(2, max_weight + 1)):
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
                        # print("Current arg: ", arg)
                        args_to_execute.append(get_eval_function(arg[1], {})) # in a math expression, representing subexpressions as tuples means they will have parenthesis around them (which is fine and needed) --> we can't do this with strings.


                    # print("args_to_execute: ", args_to_execute)


                    expr = get_expression_function(operation, (args_to_execute)) # add error checking for string DSL in this helper function since I can just continue to next arg_tuple if i have wrong data types as args
                    if expr == "ERROR":
                        continue

                    # Keep a list of what the current expression evaluates to for each example in the task.
                    curr_results = []


                    all_correct = True
                    for (input_values, output) in task_examples:
                        input_mapping = {f"x{i}": v for i, v in enumerate(input_values)}



                        expr_result = get_eval_function(expr, input_mapping) # i did error checking in arithmetic domain in this helper function 
                        
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

                    if all_correct and len(curr_results) == len(task_examples):
                        if domain == "string":
                            temp_args = []
                            temp_list = list(arg_tuple)
                            for my_arg in temp_list:

                                actual_arg = my_arg[1]
                                if type(actual_arg) == str and actual_arg[0] == "'":
                                    actual_arg = actual_arg[1:-1]
                                    temp_list2 = actual_arg.split("'")

                                    temp_string = f"Concatenate('{temp_list2[0]}', '{temp_list2[2]}')"

                                    temp_args.append(temp_string)

                                else:
                                    temp_args.append(my_arg[1])
                            temp_args = tuple(temp_args)
                            programs_found.append(f"Solution: {operation}{temp_args}\n")
                        elif domain == "arithmetic":
                            programs_found.append("Solution: " + expr)

                    if len(programs_found) == len(input_output_examples):
                        print("=====================================")
                        print("WE HAVE FOUND THE FOLLOWING PROGRAMS: ")
                        for program in programs_found:
                            print(program)
                        print("DONE")
                        exit()

    print("If we reached this point, we did not synthesize programs :(")
    return

if __name__ == "__main__":
    main()