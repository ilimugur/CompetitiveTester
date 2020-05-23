import testerFunctions
import randomizedDataFunctions as dataGenerator
import argparse

def generateInput():
    # Code input generation function here
    # Return a list of lists where contents of each list represents a line of input
    minN = 1
    maxN = 10
    minM = 0
    maxM = 10
    minW = 0
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

if __name__ == "__main__":
    desc = 'Test code against a correct solution with random cases.'
    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument('--test-dir', metavar='T', type=str, required=True)
    parser.add_argument('--num-tests-to-run', metavar='N', type=int)
    parser.add_argument('--user-code', metavar='U', type=str, required=True)
    parser.add_argument('--correct-code', metavar='C', type=str, required=True)
    args = parser.parse_args()

    numTestsToConduct = args.num_tests_to_run

    testerFunctions.run(args.test_dir, numTestsToConduct,
                        args.user_code, args.correct_code, generateInput)
