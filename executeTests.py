import os
import shutil

# Program Name. Update this according to the program name each semester
PROGRAM_NAME = "tash.c"

# Define ANSI color codes
BLUE = '\033[1;34m'
GREEN = '\033[1;32m'
RED = '\033[1;31m'
RESET = '\033[0m'

# Program and binary name
INPUT_CODE = PROGRAM_NAME
OUTPUT_BINARY = PROGRAM_NAME[:4]

# Add your required flags here
compilationFlags = ["-Wall -Werror -O" , "-Wall -Werror -O -std=c99", "-O -std=c99", "-std=c99", ""]

# Total score
totalScore = 0

# Function definitions
def compileProgram(sourceFile, outputBinary, compilationFlags):
    print(f"\n\n{BLUE}Test: Compilation (10 points){RESET}")
    for compilationFlagsToAdd in compilationFlags:
        compileCommand = "gcc " + sourceFile + " -o " + outputBinary + " " + compilationFlagsToAdd
        print(f"\n\n{BLUE}Compiling with: {compileCommand}{RESET}\n\n")
        compilationResult = os.system(compileCommand)

        if compilationResult == 0:
            print(f"{GREEN}Test: Compilation - PASSED{RESET}")
            totalScore += 10
            return

    print(f"\n\n{RED}Test: Compilation - FAILED{RESET}")

def createTestFolderAndFiles():
    print(f"\n\n{BLUE}Creating test files{RESET}")
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

# Main program
# Compilation
compileProgram(INPUT_CODE, OUTPUT_BINARY, compilationFlags)

# Create support folder and files
createTestFolderAndFiles()
cleanUpTestFolder()