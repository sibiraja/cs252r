# Bottom-Up Search -- Program Synthesis Tool

Welcome to my implementation of a Bottom-Up Search program synthesis tool! This tool is based on the paper [BUSTLE: BOTTOM-UP PROGRAM SYNTHESIS THROUGH LEARNING-GUIDED EXPLORATION](https://arxiv.org/pdf/2007.14381.pdf) by Odena et al. (Google Research Team). This implementation contains the non-machine learning part of the BUSTLE algorithm


This bottom up search algorithm can be generalized to multiple domains. This implementation contains the following domains:
- Arithmetic (operations include: +, -, *, /)
- String Manipulation (operations include: concatenation, retreiving the character at a relative left index, retreiving the character at a relative right index)

## Repository Structure
- **masterbustle.py**: This is the main script that runs the bottom up search algorithm. It takes in a domain as a command line argument and runs the bottom up search algorithm on that domain.
- **helper.py**: This script contains domain-specific helper functions that are used in the bottom up search algorithm
- The **archaicwork** and **seconditeration** folders contain old code that was used in the development of this project. They are not used in the final implementation of the bottom up search algorithm. I have kept these files in the repository for my personal reference


## Running the Code

Make sure you have python installed. Execute the `masterbustle.py` sript along with a domain passed in as a command line argument in this format:

```
python masterbustle.py <domain>
```


To run the arithmetic domain, execute the following command:

```
python masterbustle.py arithmetic
```

To run the string manipulation domain, execute the following command:

```
python masterbustle.py string
```

In `helper.py`, you can change the input and output examples that are used in the bottom up search algorithm by simply editing the function called `retrieve_arithmetic_io_examples()` or `retrieve_string_io_examples()`. The input and output examples are stored as a list of lists. Each inner list contains the input and output examples for a specific task. Within each inner list, there is a sequence of tuples, each representing the specific input and output example. The first element of a tuple is a list of inputs, and the second element of the tuple is the output.

There are some specific peices of information related to implementation that are helpful to know if you'd like to play around with the code yourself, which I discuss below.


## Implementation Overview

### Dependencies
`masterbustle.py` begins by importing the following libraries: `sys`, `itertools`, and `tqdm`. The `sys` library is used to retrieve the domain that is passed in as a command line argument. The `itertools` library is used to generate all possible programs of a certain length. The `tqdm` library is used to display a progress bar in the terminal.

### Code Structure

- `masterbustle.py` closely follows the algorithm presented in the BUSTLE paper. As much as possible, variable names correspond closely to what is presented in `Algorithm 1` in the paper.
- `helper.py` contains domain-specific helper functions that are used by `masterbustle.py` in the bottom up search algorithm. Purposes of such functions include initializing the input and output examples, formatting programs as expressions, and evaluating such expressions.


**Note**: it's important to understand that the bottom up synthesis tool generates programs of a certain weight and the current implementation is extremely brute-force. From my initial experiments running on a laptop with 16GB RAM, I found we can find programs in the arithmetic domain of up to weight 7, while we can find programs in the string manipulation domain of up to weight 5. As such, I have initialized the `max_weight` variable, which represents exactly this weight parameter, to be 5 in both domains for fast runtime on both domains (again, it is completely possible to do 7 in arithmetic, but note that you should only do as such when running higher weighted tasks. Otherwise, even if you have simpler tasks in the same batch, the entire program will still take quite some time to run before you can see the results of even the simple tasks). You can change this variable to a higher value if you'd like to experiment with larger programs, but be warned that the program will take a long time to run and may crash your computer if you don't have enough memory. 


## Example Outputs

In the event of a successful program synthesis, the bottom up search will output the programs that it has found via the terminal. For example, if you run the bottom up search on the arithmetic domain with the following input and output examples:

```python
arithmetic_input_output_examples = [
        [([1,2], 3), ([2,3], 5), ([3,4], 7), ([4,5], 9)], # add 2 numbers
        [([1,2], 2), ([2,3], 6), ([3,4], 12), ([4,5], 20)], # multiply 2 numbers
        [([1,2], -1), ([2,3], -1), ([3,4], -1), ([4,6], -2)], # subtract 2 numbers
        [([1,2], 0), ([6,3], 2), ([10,4], 2), ([49,7], 7)], # divide 2 numbers
    ]
```

The bottom up search will output the following in your terminal:

```
=====================================
WE HAVE FOUND THE FOLLOWING PROGRAMS: 
Solution: (x0 + x1)
Solution: (x0 * x1)
Solution: (x0 - x1)
Solution: (x0 // x1)
DONE
```

In the event that the bottom up search is unable to find a program that satisfies all of the input and output examples, it will print the following output in your terminal:

```
If we reached this point, we did not synthesize programs :(
```


**That's it from me! Enjoy and happy Synthesizing!**