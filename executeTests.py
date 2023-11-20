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
YELLOW = '\033[1;33m'
RESET = '\033[0m'

# Scores to assign
TOTAL_NORMAL_TEST_CASES = 30
MAXIMUM_TEST_CASE_POINTS = 45
TEST_CASE_POINTS = MAXIMUM_TEST_CASE_POINTS / TOTAL_NORMAL_TEST_CASES
COMPILATION_POINTS = 10
LONG_COMMAND_POINTS = 5
FAILURE_POINTS = 0
TEST_TIMEOUT = 10

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
TEST_CASE_7 = "Test Case 7: Valid ls command in Interactive Mode"
TEST_CASE_8 = "Test Case 8: Invalid ls commmand in Interactive Mode"
TEST_CASE_9 = "Test Case 9: Start Batch Mode with a file that does not exist"
TEST_CASE_10 = "Test Case 10: Start Batch Mode with multiple valid files"
TEST_CASE_11 = "Test Case 11: Test echo command with variable whitespaces in Interactive Mode"
TEST_CASE_12 = "Test Case 12: Test echo command with variable whitespaces in Batch Mode"
TEST_CASE_13 = "Test Case 13: Test output redirection without specifying output file in Interactive Mode"
TEST_CASE_14 = "Test Case 14: Test output redirection without specifying output file in Batch Mode"
TEST_CASE_15 = "Test Case 15: Test output redirection with multiple output files in Interactive Mode"
TEST_CASE_16 = "Test Case 16: Test output redirection with multiple output files in Batch Mode"
TEST_CASE_17 = "Test Case 17: Test output redirection with multiple redirection symbols '>' in Interactive Mode"
TEST_CASE_18 = "Test Case 18: Test output redirection with multiple redirection symbols '>' in Batch Mode"
TEST_CASE_19 = "Test Case 19: Normal redirection in Interactive Mode"
TEST_CASE_20 = "Test Case 20: Normal redirection in Batch Mode"
TEST_CASE_21 = "Test Case 21: Test bad redirection (Nothing to left of redirection symbols '>') in Interactive Mode"
TEST_CASE_22 = "Test Case 22: Test bad redirection (Nothing to left of redirection symbols '>') in Batch Mode"
TEST_CASE_23 = "Test Case 23: Test bad parallel commands (Nothing to the left of parallel symbol '&') in Interactive Mode"
TEST_CASE_24 = "Test Case 24: Test bad parallel commands (Nothing to the left of parallel symbol '&') in Batch Mode"
TEST_CASE_25 = "Test Case 25: Test normal parallel commands in Interactive Mode"
TEST_CASE_26 = "Test Case 26: Test normal parallel commands in Batch Mode"
TEST_CASE_27 = "Test Case 27: Test normal redirection with parallel commands with parallel symbol '&' at end in Interactive Mode"
TEST_CASE_28 = "Test Case 28: Test normal redirection with parallel commands with parallel symbol '&' at end in Batch Mode"
TEST_CASE_29 = "Test Case 29: Test redirection and parallel commands without spacing between symbols in Interactive Mode"
TEST_CASE_30 = "Test Case 30: Test redirection and parallel commands without spacing between symbols in Batch Mode"
TEST_CASE_31 = "Test Case 31: Test long command in Batch Mode"

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

    # Remove the compiled binary
    os.remove(OUTPUT_BINARY)

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

    maximumScore = MAXIMUM_TEST_CASE_POINTS + COMPILATION_POINTS + LONG_COMMAND_POINTS
    print(f"\n\n{BLUE}Maximum Possible Score: {maximumScore}{RESET}")

    if totalScore >= maximumScore - (maximumScore * 0.1):
        print(f"{GREEN}Your Score: {totalScore}{RESET}")

    elif totalScore >= maximumScore - (maximumScore * 0.3):
        print(f"{YELLOW}Your Score: {totalScore}{RESET}")

    else:
        print(f"{RED}Your Score: {totalScore}{RESET}")

# Testing Functions

# Test Compilation
def compileProgram(sourceFile, outputBinary, compilationFlags):
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_0+f" ({COMPILATION_POINTS} points){RESET}")
    commandIdx = 0

    for compilationFlagsToAdd in compilationFlags:
        compileCommand = "gcc " + sourceFile + " -o " + outputBinary + " " + compilationFlagsToAdd
        print(f"\n\n{BLUE}Compiling with: {compileCommand}{RESET}\n\n")
        returnCode, output, error = runCommandWithTimeout(compileCommand, timeout=TEST_TIMEOUT)

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
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

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
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

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
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_3+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_3] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'3.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_3+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
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
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_4+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_4] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'4.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_4+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
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
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_5+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_5] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'5.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_5+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
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
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_6+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_6] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'6.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_6+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_6] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_6+f" - PASSED{RESET}")
        testResults[TEST_CASE_6] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_7
def testCase7():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_7+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'7.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_7+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_7] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'7.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_7+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_7] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_7+f" - PASSED{RESET}")
        testResults[TEST_CASE_7] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_8
def testCase8():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_8+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'8.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_8+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_8] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'8.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_8+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_8] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_8+f" - PASSED{RESET}")
        testResults[TEST_CASE_8] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_9
def testCase9():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_9+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'does_not_exist.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_9+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_9] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'9.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_9+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_9] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_9+f" - PASSED{RESET}")
        testResults[TEST_CASE_9] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_10
def testCase10():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_10+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'10.in'} {TEST_CASES_PATH+'case'+'10.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_10+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_10] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'10.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_10+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_10] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_10+f" - PASSED{RESET}")
        testResults[TEST_CASE_10] = PASSED_STRING
        return TEST_CASE_POINTS

# TEST_CASE_11
def testCase11():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_11+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'11.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_11+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_11] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'11.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_11+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_11] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_11+f" - PASSED{RESET}")
        testResults[TEST_CASE_11] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_12
def testCase12():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_12+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'12.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_12+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_12] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'12.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_12+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_12] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_12+f" - PASSED{RESET}")
        testResults[TEST_CASE_12] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_13
def testCase13():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_13+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'13.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_13+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_13] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'13.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_13+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_13] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_13+f" - PASSED{RESET}")
        testResults[TEST_CASE_13] = PASSED_STRING
        return TEST_CASE_POINTS

# TEST_CASE_14
def testCase14():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_14+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'14.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_14+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_14] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'14.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_14+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_14] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_14+f" - PASSED{RESET}")
        testResults[TEST_CASE_14] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_15
def testCase15():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_15+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'15.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_15+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_15] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'15.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_15+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_15] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_15+f" - PASSED{RESET}")
        testResults[TEST_CASE_15] = PASSED_STRING
        return TEST_CASE_POINTS

# TEST_CASE_16
def testCase16():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_16+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'16.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_16+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_16] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'16.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_16+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_16] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_16+f" - PASSED{RESET}")
        testResults[TEST_CASE_16] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_17
def testCase17():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_17+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'17.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_17+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_17] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'17.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_17+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_17] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_17+f" - PASSED{RESET}")
        testResults[TEST_CASE_17] = PASSED_STRING
        return TEST_CASE_POINTS

# TEST_CASE_18
def testCase18():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_18+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'18.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_18+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_18] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'18.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_18+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_18] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_18+f" - PASSED{RESET}")
        testResults[TEST_CASE_18] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_19
def testCase19():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_19+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'19.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_19+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_19] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'19.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_19+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_19] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_19+f" - PASSED{RESET}")
        testResults[TEST_CASE_19] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_20
def testCase20():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_20+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'20.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_20+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_20] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'20.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_20+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_20] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_20+f" - PASSED{RESET}")
        testResults[TEST_CASE_20] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_21
def testCase21():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_21+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'21.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_21+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_21] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'21.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_21+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_21] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_21+f" - PASSED{RESET}")
        testResults[TEST_CASE_21] = PASSED_STRING
        return TEST_CASE_POINTS

# TEST_CASE_22
def testCase22():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_22+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'22.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_22+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_22] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'22.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_22+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_22] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_22+f" - PASSED{RESET}")
        testResults[TEST_CASE_22] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_23
def testCase23():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_23+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'23.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_23+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_23] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'23.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_23+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_23] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_23+f" - PASSED{RESET}")
        testResults[TEST_CASE_23] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_24
def testCase24():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_24+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'24.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_24+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_24] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(error, TEST_CASES_PATH+'case'+'24.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_24+f" - FAILED{RESET}")
        print("Your Output:")
        print(error)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_24] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_24+f" - PASSED{RESET}")
        testResults[TEST_CASE_24] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_25
def testCase25():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_25+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'25.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_25+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_25] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'25_1.out')

    if result == 0:
        previousExpectedOutput = expectedOutput
        result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'25_2.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_25+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        print("\nOR\n")
        print(previousExpectedOutput)
        testResults[TEST_CASE_25] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_25+f" - PASSED{RESET}")
        testResults[TEST_CASE_25] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_26
def testCase26():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_26+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'26.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_26+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_26] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'26_1.out')

    if result == 0:
        previousExpectedOutput = expectedOutput
        result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'26_2.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_26+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        print("\nOR\n")
        print(previousExpectedOutput)
        testResults[TEST_CASE_26] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_26+f" - PASSED{RESET}")
        testResults[TEST_CASE_26] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_27
def testCase27():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_27+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'27.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_27+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_27] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'27.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_27+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_27] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_27+f" - PASSED{RESET}")
        testResults[TEST_CASE_27] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_28
def testCase28():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_28+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'28.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_28+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_28] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'28.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_28+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_28] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_28+f" - PASSED{RESET}")
        testResults[TEST_CASE_28] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_29
def testCase29():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_29+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash < {TEST_CASES_PATH+'case'+'29.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_29+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_29] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'29.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_29+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_29] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_29+f" - PASSED{RESET}")
        testResults[TEST_CASE_29] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_30
def testCase30():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_30+f" ({TEST_CASE_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'30.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_30+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_30] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'30.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_30+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_30] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_30+f" - PASSED{RESET}")
        testResults[TEST_CASE_30] = PASSED_STRING
        return TEST_CASE_POINTS
    
# TEST_CASE_31 (Long Test Case)
def testCase31():
    global testResults
    print(f"\n\n{PURPLE}"+TEST_CASE_31+f" ({LONG_COMMAND_POINTS} points){RESET}")
    command = f"./tash {TEST_CASES_PATH+'case'+'31.in'}"
    returnCode, output, error = runCommandWithTimeout(command, timeout=TEST_TIMEOUT)

    if returnCode == -1:
        print(f"{RED}"+TEST_CASE_31+f" - FAILED (Time exceeded){RESET}")
        testResults[TEST_CASE_31] = FAILED_TLE_STRING
        return FAILURE_POINTS
    
    result, expectedOutput = compareOutput(output, TEST_CASES_PATH+'case'+'31.out')
    
    if result == 0:
        print(f"{RED}"+TEST_CASE_31+f" - FAILED{RESET}")
        print("Your Output:")
        print(output)
        print("Expected Output:")
        print(expectedOutput)
        testResults[TEST_CASE_31] = FAILED_STRING
        return FAILURE_POINTS
    
    else:
        print(f"{GREEN}"+TEST_CASE_31+f" - PASSED{RESET}")
        testResults[TEST_CASE_31] = PASSED_STRING
        return LONG_COMMAND_POINTS
    
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
totalScore = totalScore + testCase7() # TEST_CASE_7
totalScore = totalScore + testCase8() # TEST_CASE_8
totalScore = totalScore + testCase9() # TEST_CASE_9
totalScore = totalScore + testCase10() # TEST_CASE_10
totalScore = totalScore + testCase11() # TEST_CASE_11
totalScore = totalScore + testCase12() # TEST_CASE_12
totalScore = totalScore + testCase13() # TEST_CASE_13
totalScore = totalScore + testCase14() # TEST_CASE_14
totalScore = totalScore + testCase15() # TEST_CASE_15
totalScore = totalScore + testCase16() # TEST_CASE_16
totalScore = totalScore + testCase17() # TEST_CASE_17
totalScore = totalScore + testCase18() # TEST_CASE_18
totalScore = totalScore + testCase19() # TEST_CASE_19
totalScore = totalScore + testCase20() # TEST_CASE_20
totalScore = totalScore + testCase21() # TEST_CASE_21
totalScore = totalScore + testCase22() # TEST_CASE_22
totalScore = totalScore + testCase23() # TEST_CASE_23
totalScore = totalScore + testCase24() # TEST_CASE_24
totalScore = totalScore + testCase25() # TEST_CASE_25
totalScore = totalScore + testCase26() # TEST_CASE_26
totalScore = totalScore + testCase27() # TEST_CASE_27
totalScore = totalScore + testCase28() # TEST_CASE_28
totalScore = totalScore + testCase29() # TEST_CASE_29
totalScore = totalScore + testCase30() # TEST_CASE_30
totalScore = totalScore + testCase31() # TEST_CASE_31

# Cleaning
cleanUpTestFolder()

# Print test results
printResults(totalScore)

# Close the log file when you're done
# logFile.close()