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

Make sure you have python installed. Execute the masterbustle.py sript along with a domain passed in as a command line argument in this format:

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

In **helper.py**, you can change the input and output examples that are used in the bottom up search algorithm by simply editing the function called **retrieve_arithmetic_io_examples()** or **retrieve_string_io_examples()**. The input and output examples are stored as a list of lists. Each inner list contains the input and output examples for a specific task. Within each inner list, there is a sequence of tuples, each representing the specific input and output example. The first element of a tuple is a list of inputs, and the second element of the tuple is the output.

There are some specific peices of information related to implementation that are helpful to know if you'd like to play around with the code yourself, which I discuss below.


## Implementation Overview



### Example Outputs