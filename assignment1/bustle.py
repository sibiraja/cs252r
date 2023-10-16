# scm.py creates an interpreter

import itertools

# First let's define some input output examples

# Target program is to add the 2 numbers and multiply the result by 2
input_output_examples = [ ([1,2], 6), ([2,3], 10), ([3,4], 14), ([4,5], 18) ]

operations = ["+", "*"]

# E maps integer weights to terms with that weight
E = {}


# inputs and constants have weight 1
E[1] = ["1", "2", "3", "4", "5"]


# have another mapping that maps terms to their weights
args_to_weights = {"1": 1, "2": 1, "3": 1, "4": 1, "5": 1}



# let's define a max weight that will be used to terminate the search
max_weight = 10

# loop over all possible term weights
for w in range(2, max_weight):

    # loop over all possible operations
    for op in operations:
        # print(op)

        # n = op.arity --> what is this? is this the number of arguments that the operation takes? hard code as just 2 for now?
        n = 2
        A = []
        
        # generate all possible argument tuples using itertools. Then for each tuple, check if the length is n and the sum of the weights is w - 1. If so, add to A
        # do this by getting all the values in E and then using itertools to generate all possible permutations of length n, and then reference the args_to_weights mapping to get the weights of each argument in the tuple
        # then check if the sum of the weights is w - 1. If so, add to A

        # get all the values in E
        values_in_E = []
        for value in E.values():
            values_in_E.extend(value)
        
        # generate all possible permutations of length n
        permutations = list(itertools.permutations(values_in_E, n))
        # print(permutations)

        # for each permutation, check if the sum of the weights is w - 1. If so, add to A
        for permutation in permutations:
            sum_of_weights = 0
            for arg in permutation:
                sum_of_weights += args_to_weights[arg]
            if sum_of_weights == w - 1:
                A.append(permutation)



        # for all argument tuples in A:
        for arg_tuple in A:

            num_satsified = 0
            target_num_satisfied = len(input_output_examples)
            expression = f"{arg_tuple[0]} {op} {arg_tuple[1]}"
            print(expression)

            # for execute the operation on the argument tuple.
            try:
                result = eval(expression)
            except Exception as e:
                # Handle exceptions (e.g., if the program is invalid).
                print("Exception")
                continue

            # if the result of the execution has a weight that has not been encountered before, add it to the mapping E
            if w not in E:
                E[w] = [expression]
                # also add the result to the args_to_weights mapping
                args_to_weights[expression] = w

            for io_example in input_output_examples:
                # if the result of the execution is the output example that we are trying to satisfy, then we are done.
                    # return the program that we have found
                if result == io_example[1]:
                    # print(f"Found a solution: {expression}")
                    num_satsified += 1

            if num_satsified == target_num_satisfied:
                print(expression)
                exit()