For bustle to be able to handle 2 domains, we can create some helper functions for each part of the code that is relevant the the DSL
such as initializing constants, operators, etc. And based on CLI input, we can have a if condition that will call the relevant helper function


After I implement a working version of stringbustle, I need to combine everything into 1 masterbustle.py file.

Here's how I should go about this:
- analyze stringbustle.py and mathbustle.py and jot down EVERY place where they differ.
- Then create a helper function for EACH difference.
- The helper functions should take in a 0 or 1 and depending on if the arg is a 0 or 1, we execute code for the corresponding task domain {0: arithmetic, 1: string}
- Then, we define a main function in masterbustle.py that takes in a 0 or 1 via CLI and calls the relevant helper functions in another file (e.g. helper.py)