import subprocess
import os

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

