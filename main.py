import testerFunctions
import randomizedDataFunctions as dataGenerator

# The implementation below generates output for the following problem:
# https://codeforces.com/contest/894/problem/E
#def generateInput():
#    minN = 1
#    maxN = maxM = 1000000
#    minM = minW = 0
#    maxW = 100000000
#    n, E = dataGenerator.getGraph(minN, maxN, minM, maxM, True, minW, maxW,
#                                  isSimpleGraph = False, hasSelfLoops = True,
#                                  isDirected = True, isConnected = False,
#                                  isDAG = False)
#
#    m = len(E)
#    start = dataGenerator.getRandomInteger(1, n)
#
#    inputStructure = []
#    inputStructure.append( [ n, m ] )
#    inputStructure += E
#    inputStructure.append( [ start ] )
#
#    return inputStructure

def generateInput():
    # Implement your input generation function here
    # Return a list of lists where contents of each list represents a line of input
    # The implementation above is left here as an example
    return [[]]

if __name__ == "__main__":
    testerFunctions.main(generateInput)
