import os
import subprocess
import argparse

def initialize(userCodeFilePath, correctCodeFilePath,
               userExecutablePath, correctExecutablePath):
    subprocess.check_output(['g++', '-g', '-o',
                             userExecutablePath, userCodeFilePath])
    subprocess.check_output(['g++', '-o',
                             correctExecutablePath, correctCodeFilePath])

def printInputToFile(inputFileLocation, inputStructure):
    f = open(inputFileLocation, 'w')
    for lineList in inputStructure:
        s = ''
        for element in lineList:
            s += str(element) + ' '
        s.rstrip()
        s += '\n'
        f.write(s)
    f.close()

def printInputToStdout(inputStructure):
    for lineList in inputStructure:
        s = ''
        for element in lineList:
            s += str(element) + ' '
        s.rstrip()
        print(s)

def readOutputFile(outputFileLocation):
    s = ''
    with open(outputFileLocation, 'r') as f:
        for line in f:
            s += line
    return s

def generateOutput(executableFilePath, inputFilePath, outputFilePath):
    inputBytes = subprocess.check_output(['cat', inputFilePath])
    cmd = '%s < %s > %s' % (executableFilePath, inputFilePath, outputFilePath)
    os.system(cmd)

def deallocateInputStructure(inputStructure):
    for elem in inputStructure:
        for val in elem:
            del val

def executeTest(generateInput, inputFileLocation,
                userExecutablePath, correctExecutablePath,
                userOutputFileLocation, correctOutputFileLocation):
    inputStructure = generateInput()
#    print('Formed input.')
    printInputToFile(inputFileLocation, inputStructure)
#    print('Printed input to file.')
    generateOutput(userExecutablePath,
                   inputFileLocation, userOutputFileLocation)
#    print('Ran user code.')
    generateOutput(correctExecutablePath,
                   inputFileLocation, correctOutputFileLocation)
#    print('Ran correct code.')

    userOutput = readOutputFile(userOutputFileLocation)
    correctOutput = readOutputFile(correctOutputFileLocation)
    userOutput.rstrip()
    correctOutput.rstrip()
    result = (userOutput == correctOutput)
    if not result:
        print('DIFFERENT OUTPUTS DETECTED!')
        print('INPUT:')
        printInputToStdout(inputStructure)
        print('USER OUTPUT:')
        print(userOutput)
        print('CORRECT OUTPUT:')
        print(correctOutput)
        deallocateInputStructure(inputStructure)
        exit(0)

    deallocateInputStructure(inputStructure)
    return result

def run(testDirectory, numTestsToRun,
        userCodeFilePath, correctCodeFilePath, generateInput):
    inputFileLocation = '%s/input.txt' % testDirectory
    userOutputFileLocation = '%s/output-user.txt' % testDirectory
    correctOutputFileLocation = '%s/output-correct.txt' % testDirectory
    userExecutablePath = '%s/user.out' % testDirectory
    correctExecutablePath = '%s/correct.out' % testDirectory
    initialize(userCodeFilePath, correctCodeFilePath,
               userExecutablePath, correctExecutablePath)

    t = 1
    while numTestsToRun is None or t <= numTestsToRun:
        try:
            print('Conducting test #%d:' % t)
            executeTest(generateInput, inputFileLocation,
                        userExecutablePath, correctExecutablePath,
                        userOutputFileLocation, correctOutputFileLocation)
            print('SUCCESSFUL!')
        except KeyboardInterrupt:
            print('TESTING TERMINATED DUE TO KEYBOARD INTERRUPT!')
            exit(0)
        t += 1

def generateTests(testDirectory, numTestsToRun, generateInput):
    for i in range(1, numTestsToRun+1):
        inputFileLocation = '%s/input-%d.txt' % (testDirectory, i)
        inputStructure = generateInput()
        printInputToFile(inputFileLocation, inputStructure)
        print("Printed test case #%d to %s." % (i, inputFileLocation))

def main(generateInput):
    desc = 'Test code against a correct solution with random cases.'
    parser = argparse.ArgumentParser(description = desc)
    parser.add_argument('--test-dir', metavar='T', type=str, required=True)
    parser.add_argument('--num-tests', metavar='N', type=int)
    parser.add_argument('--user-code', metavar='U', type=str)
    parser.add_argument('--correct-code', metavar='C', type=str)
    parser.add_argument('--just-generate-tests', action='store_true')
    args = parser.parse_args()

    numTestsToConduct = args.num_tests

    if args.just_generate_tests:
        if numTestsToConduct == None:
            numTestsToConduct = 1
        generateTests(args.test_dir, numTestsToConduct, generateInput)
    else:
        if args.user_code is None:
            print("Missing user's source code to be tested! Terminating...")
            exit(0)
        if args.correct_code is None:
            print("Missing correct implementation to test user's code against! Terminating...")
            exit(0)
        run(args.test_dir, numTestsToConduct,
            args.user_code, args.correct_code, generateInput)
