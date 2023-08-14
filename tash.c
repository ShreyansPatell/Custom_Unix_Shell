/**
 * @brief: tash.c
 * 
 * @paragraph: Description - This is an implementation of a user-made shell. We are calling it tash (TexAs-SHell). Feel free to play around with it. This is a project developed toward the requirements of Project-1 in the course CS 5348 : Operating Systems Concepts.
 * 
 * @authors: Shreyans Patel (SSP210009), Karan Jariwala (KHJ200000).
 */

//Include supporting file.
#include "lib.h"
#include "def.h"
#include "funct.c"

/**
 * @brief: main.
 * @details: The main function of tash. This is the file that is to be compiled and executed.
 * @param: iArgc (Input) - The number of input arguments passed while executing "./tash". "./tash" counts too.
 * @param: iArgv (Input) - Array of argument strings.
 * @return int.
 */
int main(int iArgc, char** iArgv)
{
    modifyPath(DEFAULT_PATH);   //Set path variable to default "/bin".

    initTash(iArgc,iArgv);   //Initialize tash and derive operation mode.

    //Exit Shell
    return 0;
}