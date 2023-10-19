# Assignment 1


## Plan:

1. Read BUSTLE paper's section on bottom up enumerative search
2. Read relevant lectures on Armando's MIT course
3. Begin thinking through the code



### Notes from BUSTLE paper
"Given a specification of a program’s intended behavior (in this paper given by input-output examples), BUSTLE performs bottom-up enumerative search for a satisfying program



## Notes from Armando's course (Lectures 2 and 3)
- Bottom up search still involves constructing an AST, but we construct it from the bottom up. We start with the leaves, and then build up the tree from there.

- Need to describe the ASTs in the form of a context free grammar. This is because we need to be able to generate the ASTs.



### Getting started:

Bustle algorithm

Input: Input-output examples
Output: A program P that satisfies the examples

Auxillary Data: : Supported operations Ops, supported properties Props, and a model M trained using Props as described in Section 3.1
DO WE HAVE TO WORRY ABOUT THE MODEL??? --> No


Step 1: E is a dictionary that maps integer weights to terms with that weight

Step 2: Extract constants

Step 3: get property signature for the





Start writing BUSTLE and trying to print out all the possible enumerated expressions first, don't actually evaluate them yet

Once I get the expression enumeration working, then I can start to think about how to evaluate them --> This is when the scheme interpreter comes in



For now, start with simple input output examples with basic operations and constants/primitives like addition and multiplication to see if the enumeration works

Do this later
To run it on the actual scheme subset and the string manipulation subset, we can load in those environment subsets into the interpreter and then evaluate the expressions in those environments






### Plan of Action:
1. First get the enumeration working for simple input output examples



### Integrete Scheme test data
1. Parse data and extract operations and constants
2. Figure out how to create a linked list representation of the AST to pass into the interpreter
3. Pass in the linked list for evaluation in the interpreter