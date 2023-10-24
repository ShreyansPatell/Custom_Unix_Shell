import os
import shutil
import subprocess
# import sys

# Program Name. Update this according to the program name each semester
PROGRAM_NAME = "tash.c"
# LOG_FILE = "gradingLog.txt"

# Open the log file for writing
# logFile = open(LOG_FILE, 'w')

# Redirect standard output and standard error to the log file
# sys.stdout = logFile
# sys.stderr = logFile

# Define ANSI color codes
BLUE = '\033[1;34m'
GREEN = '\033[1;32m'
RED = '\033[1;31m'
PURPLE = '\033[1;35m'
BLACK = '\033[1;30m'
RESET = '\033[0m'

# Scores to assign
TOTAL_NORMAL_TEST_CASES = 25
MAXIMUM_TEST_CASE_POINTS = 50
TEST_CASE_POINTS = MAXIMUM_TEST_CASE_POINTS / TOTAL_NORMAL_TEST_CASES
COMPILATION_POINTS = 10
LONG_COMMAND_POINTS = 5
PARTIAL_POINTS = MAXIMUM_TEST_CASE_POINTS / (TOTAL_NORMAL_TEST_CASES * 2)
FAILURE_POINTS = 0

# Program and binary name
INPUT_CODE = PROGRAM_NAME
OUTPUT_BINARY = PROGRAM_NAME[:4]
TEST_CASES_PATH = "testcases/"
PASSED_STRING = f"{GREEN}PASSED{RESET}"
FAILED_STRING = f"{RED}FAILED{RESET}"
FAILED_TLE_STRING = f"{RED}FAILED (TLE){RESET}"
PARTIAL_STRING = f"{BLUE}PARTIALLY PASSED{RESET}"

# Add your required flags here
compilationFlags = ["-Wall -Werror -O" , "-Wall -Werror -O -std=c99", "-O -std=c99", "-std=c99", ""]

# Test cases
TEST_CASE_0 = "Test Case 0: Code Compilation"
TEST_CASE_1 = "Test Case 1: Inbuilt Command in Interactive Mode -> path"
TEST_CASE_2 = "Test Case 2: Inbuilt Command in Batch Mode -> path"
TEST_CASE_3 = "Test Case 3: Inbuilt Command in Interactive Mode -> cd"
TEST_CASE_4 = "Test Case 4: Inbuilt Command in Batch Mode -> cd"
TEST_CASE_5 = "Test Case 5: Inbuilt Command in Interactive Mode -> exit"
TEST_CASE_6 = "Test Case 6: Inbuilt Command in Batch Mode -> exit"

# Global variables
totalScore = 0
testResults = {}

# Helper Functions
def createTestFolderAndFiles():
    print(f"{BLUE}Creating test files{RESET}")
    # Create a directory named 'test'
    os.makedirs('test', exist_ok=True)

    # Create 4 empty files inside the 'test' folder
    for i in range(1, 5):
        filePath = os.path.join('test', f'test{i}')
        open(filePath, 'w').close()

def cleanUpTestFolder():
    print(f"\n{BLUE}Cleaning test files{RESET}\n")
    # Remove the 'test' folder and its contents
    shutil.rmtree('test', ignore_errors=True)

def runCommandWithTimeout(command, timeout):
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate(timeout=timeout)
        return process.returncode, stdout.decode(), stderr.decode()
    except subprocess.TimeoutExpired:
        process.kill()
        return -1, "", "TimeoutExpired"

def compareOutput(output, expectedOutputFile):
    with open(expectedOutputFile, 'r') as f:
        expectedOutput = f.read()

    return (output.strip() == expectedOutput.strip()), expectedOutput

def printResults(totalScore):
    print(f"\n\n{PURPLE}Test Results:{RESET}\n")

    for key, value in testResults.items():
        print(f"{BLACK}" + key, value + f"{RESET}")

    print("\n\nTotal Points: ", totalScore)

# Testing Functions

# Test Compilation
def compileProgram(sourceFile, outputBinary, compilationFlags):
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_0+f" ({COMPILATION_POINTS} points){RESET}")
    commandIdx = 0

    for compilationFlagsToAdd in compilationFlags:
        compileCommand = "gcc " + sourceFile + " -o " + outputBinary + " " + compilationFlagsToAdd
        print(f"\n\n{BLUE}Compiling with: {compileCommand}{RESET}\n\n")
        returnCode, output, error = runCommandWithTimeout(compileCommand, timeout=10)

        if returnCode == 0:
            if commandIdx > 1:
                print(f"{GREEN}"+TEST_CASE_0+f" - PASSED (Penalty for not following compilation instuctions from PDF){RESET}")
                testResults[TEST_CASE_0] = PARTIAL_STRING
                return (COMPILATION_POINTS - 2)
            
            print(f"{GREEN}"+TEST_CASE_0+f" - PASSED{RESET}")
            testResults[TEST_CASE_0] = PASSED_STRING
            return COMPILATION_POINTS
        
        print(error)
        commandIdx = commandIdx + 1

    print(f"{RED}"+TEST_CASE_0+f" - FAILED{RESET}")
    testResults[TEST_CASE_0] = FAILED_STRING
    return FAILURE_POINTS

# TEST_CASE_1
def testCase1():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_1+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'1.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=10)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_1+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_1] = FAILED_TLE_STRING
        return FAILURE_POINTS

    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'1.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_1+f" - FAILED{RESET}")
        testResults[TEST_CASE_1] = FAILED_STRING
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_1+f" - PASSED{RESET}")
        testResults[TEST_CASE_1] = PASSED_STRING
        return TEST_CASE_POINTS

# TEST_CASE_2
def testCase2():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_2+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'2.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=10)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_2+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_2] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'2.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_2+f" - FAILED{RESET}")
        testResults[TEST_CASE_2] = FAILED_STRING
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_2+f" - PASSED{RESET}")
        testResults[TEST_CASE_2] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_3
def testCase3():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_3+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'3.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=10)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_3+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_3] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'3.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_3+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_3] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_3+f" - PASSED{RESET}")
        testResults[TEST_CASE_3] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_4
def testCase4():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_4+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'4.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=10)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_4+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_4] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'4.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_4+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_4] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_4+f" - PASSED{RESET}")
        testResults[TEST_CASE_4] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_5
def testCase5():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_5+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'5.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=10)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_5+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_5] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'5.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_5+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_5] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_5+f" - PASSED{RESET}")
        testResults[TEST_CASE_5] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_6
def testCase6():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_6+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'6.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=10)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_6+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_6] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'6.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_6+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_6] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_6+f" - PASSED{RESET}")
        testResults[TEST_CASE_6] = PASSED_STRING
        return TEST_CASE_POINTS

# Main program
# Create support folder and files
createTestFolderAndFiles()

# Test compilation
totalScore = totalScore + compileProgram(INPUT_CODE, OUTPUT_BINARY, compilationFlags)

# Test normal cases
totalScore = totalScore + testCase1() # TEST_CASE_1
totalScore = totalScore + testCase2() # TEST_CASE_2
totalScore = totalScore + testCase3() # TEST_CASE_3
totalScore = totalScore + testCase4() # TEST_CASE_4
totalScore = totalScore + testCase5() # TEST_CASE_5
totalScore = totalScore + testCase6() # TEST_CASE_6

# Print test results
printResults(totalScore)

# Cleaning
cleanUpTestFolder()

# Close the log file when you're done
# logFile.close()