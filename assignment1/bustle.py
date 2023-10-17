import itertools

# First let's define some input output examples

# This is a list of lists. Each inner list is a list of tuples representing IO examples for a given task. Each tuple is an input output example. 
# The first element of the tuple is the input and the second element is the output
arithmetic_input_output_examples = [
    [([1,2], 3), ([2,3], 5), ([3,4], 7), ([4,5], 9)], # add 2 numbers
]


# Each operation is a tuple where the first element is the function and the second element is the arity of the function and third argument is name of operator (for debugging purposes)
addition = ( lambda x, y: x + y , 2, "ADD" )
# subtraction = ( lambda x, y: x - y , 2, "SUBTRACT" )
multiplication = ( lambda x, y: x * y , 2, "MULTIPLY" )
# division = ( lambda x, y: x // y , 2 , "DIVIDE" )

operations = [addition, multiplication]

# E maps integer weights to terms with that weight
E = {}


# inputs and constants have weight 1
E[1] = []

# get all the inputs and constants and add them to E
for task in arithmetic_input_output_examples:
    for io_example in task:
        for element in io_example[0]:
            if str(element) not in E[1]:
                E[1].append(element)

print(E)

# have another mapping that maps arguments to their weights (essentially reverse of E)
args_to_weights = {}
for weight in E:
    for element in E[weight]:
        args_to_weights[element] = weight

print(args_to_weights)

# exit()


max_weight = 6


# loop over all possible term weights
for w in range(2, max_weight + 1):
    # print("new W: ", w)

    # loop over all possible operations
    for operation_tuple in operations:
        operation = operation_tuple[0]
        n_op_arity = operation_tuple[1]

        # A holds all the argument tuples that have a total weight of w - 1
        A = []

        # generate all possible argument tuples using itertools. Then for each tuple, check if the length is n and the sum of the weights is w - 1. If so, add to A
        # first do this by getting all the values in E and then using itertools to generate all possible permutations of length n, and then reference the args_to_weights mapping to get the weights of each argument in the tuple
        # then check if the sum of the weights is w - 1. If so, add to A

        # get all the values in E
        values_in_E = []
        for value in E.values():
            values_in_E.extend(value)

        # generate all possible permutations of length n
        permutations = list(itertools.permutations(values_in_E, n_op_arity)) # it would be good to type check here for better efficiency, but I can implement this later

        # print("FOR A WEIGHT OF ", w, " AND OPERATION ", operation, "WE HAVE THE FOLLOWING PERMUTATIONS: ", permutations)
        # print(permutations)
        # print("=====================================")

        # for each permutation, check if the sum of the weights is w - 1. If so, add to A
        for permutation in permutations:
            # print(permutation)
            sum_of_weights = 0
            for arg in permutation:
                # print(arg)
                sum_of_weights += args_to_weights[arg]
                # print("WEIGHT IS NOW: ", sum_of_weights)
            if sum_of_weights == w - 1:
                # print("We are looking for a weight of ", w-1, " and we have a permutation of weight ", sum_of_weights, " that satisfies this weight requirement")
                # print("THIS PERMUTATION SATISFIES THE WEIGHT REQUIREMENT: ", permutation, "of weight ", w-1)
                A.append(permutation)

        # print("FOR A WEIGHT OF ", w, " AND OPERATION ", operation, "WE HAVE THE FOLLOWING ARGUMENT TUPLES: ", A)

        # print(A)

        # for all argument tuples in A
        for arg_tuple in A:

            number_of_satisfied_examples = 0 # this is the number of input output examples that expression made from the current argument tuple and the current operation satisfies
            target_number_of_satisfied_examples = len(task) # this is the total number of input output examples that we are trying to satisfy for the current task

            # make the expression in python syntax
            current_expression = f"({operation_tuple[2]} {arg_tuple[0]} {arg_tuple[1]})"

            # try and execute the expression
            try:
                result = operation(*arg_tuple)
                print("CURRENT EXPRESSION: ", current_expression, "RESULT OF EXPRESSION: ", result)
                # print("RESULT OF EXPRESSION IS : ", result)
            except Exception as e:
                # Handle exceptions (e.g., if the program is invalid).
                print("Exception")
                continue


            # loop through all input output examples and test the result of our expression against the output of the input output example
            # does this mean I have to evaluate the expression on the inputs of the input output example?
            # TODO: Does this mean the expression I build needs to be a lambda function itself, and I need to store lambda functions in E instead of actual values (except for constants and inputs)?
            # TODO: What should I even store in E, how should I make the expression, and how do I check the evaluation of my expression against an IO example?
            # because right now, I have an operation acting on 2 concrete arguments, but how will BUSTLE eventually output a lambda function that takes in 2 arguments?



            # if the result is not in E, add it to E OR if the result is in E but the weight is less than the current weight, then update the weight in E
            # ACTUALLY, no need for the second if check since BUSTLE by default synthesizes programs and terms from least weight to most weight





exit()
# MY OLD IMPLEMENTATION OF BUSTLE THAT DOESN'T WORK 

# ALSO TODO: Need to pass in an AST to the interpreter. So need to convert the expression to an AST. I think this is where I need to use the linked list and create new nodes

# let's define a max weight that will be used to terminate the search
max_weight = 10

# loop over all possible term weights
for w in range(2, max_weight):

    # loop over all possible operations
    for operation in operations:
        # print(op)

        # n = op.arity --> what is this? is this the number of arguments that the operation takes? hard code as just 2 for now?
        n = operation[1]
        A = []


        # TODO: define op since right now it is a tuple. I need to apply the lambda function to the arguments
        
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
            # expression = f"{arg_tuple[0]} {op} {arg_tuple[1]}"
            expression = f"({op} {arg_tuple[0]} {arg_tuple[1]})"
            print(expression)

            # for execute the operation on the argument tuple.
            try:
                result = eval(expression) # NEED TO PASS THIS INTO THE INTERPRETER FOR SCHEME EVALUATION
                print("result of eval: ", result)
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