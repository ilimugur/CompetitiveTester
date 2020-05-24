# Competitive Tester

This tiny command-line module helps a competitive programmer test their code against a working solution, using randomized blackbox tests withing the bounds provided by the user.

### Use Case

Often times when upsolving a problem a bug may be difficult to locate. Edge cases are relatively easy to figure out for most problems, but a minor bug in a complex algorithm may cause an issue `N` recursive levels deep into the execution.

You can rewrite your entire code, but there is no way to know you won't repeat the same bug, or have another one. And it's generally good practice to track the bugs in your code so that, with practice, your implementations can have fewer, or no bugs.

This tool can help with that particular challenge, especially in the context of competitive programming.

### How to use it?

To utilize this tool, you need 4 things. Namely;

- Your own, problematic implementation
- An implementation that is known to be correct
- An existing directory with appropriate permissions so that the module can use it to store files
- Overriding the `generateInput()` function in [main.py](main.py) so that it generates the particular input format you need

There is also an optional command line argument to limit the number of test cases to be generated. If no such limit is specified, the execution will continue as an infinite loop that only ends when a problematic test case is found. In that case, you can create a keyboard interrupt (e.g., <kbd>Ctrl</kbd> + <kbd>C</kbd>) to end the execution.

### generateInput():

As each problem has a different input format, I didn't want to have fixed input generator functions. Instead, for each problem you need to test, you need to implement the `generateInput()` function in [main.py](main.py) so that it produces the input you desire. It seems like a lot of manual labor at an initial glance, but this module includes a few tools to make it easier for you, which are covered below.

All this module expects you to do in terms of formatting is to use the functions available within the module to generate a valid test case, and format that test case based on your needs to finally return a list of lists `L`. Each `L[i]` represents a line of input, and each element within `L[i][j]` will be printed as such to the input file for that case, with a single space between them.

The following is a sample implementation of `generateInput()`. It prints out the inputs required by [this](https://codeforces.com/problemset/problem/894/E) problem on [Codeforces](https://www.codeforces.com).

```
def generateInput():
    minN = 1
    maxN = maxM = 1000000
    minM = minW = 0
    maxW = 100000000
    n, E = dataGenerator.getGraph(minN, maxN, minM, maxM, True, minW, maxW,
                                  isSimpleGraph = False, hasSelfLoops = True,
                                  isDirected = True, isConnected = False,
                                  isDAG = False)

    m = len(E)
    start = dataGenerator.getRandomInteger(1, n)

    inputStructure = []
    inputStructure.append( [ n, m ] )
    inputStructure += E
    inputStructure.append( [ start ] )

    return inputStructure
```

### randomizedDataFunctions.py:

In [randomizedDataFunctions.py](randomizedDataFunctions.py), which is already imported into [main.py](main.py) as `dataGenerator`, there are methods to generate a random integer, float, string and graph. The integer and float generation functions are just wrappers around `random.randint` and `random.uniform`, respectively. The string generator accepts a length and an list of allowed characters.

The graph generation function returns accepts the lower and upper bounds on the number of vertices and edges. It also accepts a flag to indicate if the graph is weighted, and if so, the lower and upper bounds of edge weights. Apart from those, it accepts the following flags, which have self-explanatory names:

- isSimpleGraph
- hasSelfLoops
- isDirected
- isConnected
- isDAG (Directed Acyclic Graph)

Remember that all the bounds in these implementations are inclusive, and all the indices generated as input data are 1-indexed.

### How does it work?

You provide the relevant inputs as the command line arguments and execute the module as shown in the sample use case given below.

```shell
python main.py --test-dir /tmp/dummyDir
               --user-code /path/to/user/code.cpp
               --correct-code /path/to/correct/code.cpp
               --num-tests-to-run 100
```

Then, your code and the correct code are compiled and stored in the directory you specified. After that, the code enters a loop where, in each iteration, a new valid test case is generated, stored as a file, and fed as input to both executables as they are run. Their outputs are stored again as separate files. Finally, the outputs are read from those files, and they are compared. If they are different, the problematic input, along with the respective outputs are printed to stdout.

The execution stops either at the first case for which there are unidentical outputs or after trying a certain amount of test cases, if such a limit on the number of tests were specified as a command line argument.

You can also use the following command to see the full list of accepted command line arguments.

```
python main.py --help
```

### What's next?

Extending the randomized data functions would be nice. Range query generation and certain tree structures are on the top of my list in that area. It can be extended even further if domains such as computational geometry are to be considered.

Some online judges are relatively tolerant of whitespace issues, and it would be nice to add some flexibility about that. Currently, even an extra newline character at the end of the output causes a mismatch.

In terms of the tool itself, it is a really quick and dirty implementation. It is based on my immediate needs for a particular contest problem (Yeah, I'm referring to [you](https://codeforces.com/problemset/problem/894/E) Ralph, and to your frustrating mushrooms) and it was coded for my particular development environment. It would be nice to improve the code quality and perhaps make sure that the code can be executed in different operating systems so many other developers can benefit from it.

Eventually, it would be nice to add support for other languages as well. Once the code quality is better, it would be relatively easy to separate the compilation logic and add support for various languages.

If you have the time to dive into any of these issues, feel free to send me a pull request of whatever improvement you apply.
