/**
 * @brief: funct.c
 * 
 * @paragraph: Description - Support file of funct.h. It contains all the functions declarations.
 * 
 * @authors: Shreyans Patel (SSP210009), Karan Jariwala (KHJ200000)
 */

/**
 * @brief: modifyPath.
 * @details: This is used to modify (set/update) the path variable.
 * @param: iPath (Input) - The paths to set for the path variable.
 * @return none.
 */
void modifyPath(char* iPath);

/**
 * @brief: printErrorMsg.
 * @details: This function is used to print the one and only error message.
 * @return none.
 * @note: tTemp in this function is used to avoid compilation errors since we need to use the return value of write(). This is because of the compilation instructions being passed. Unused variables are considered errors in this case.
 */
void printErrorMsg(void);

/**
 * @brief: initTash.
 * @details: Initialization of tash program. It decides the mode of runtime i.e Interactive or Batch Mode.
 * @param: iArgc (Input) - The number of input arguments passed while executing "./tash". "./tash" counts too.
 * @param: iArgv (Input) - Array of arguments.
 * @return int.
 */
void initTash(int iArgc, char** iArgv);

/**
 * @brief: initInteractive.
 * @details: Initialize interactive mode of tash.
 * @return none.
 */
void initInteractive(void);

/**
 * @brief: initBatch.
 * @details: Initialize batch mode of tash.
 * @param: iArgv (Input) - Array of argument strings.
 * @return none.
 */
void initBatch(char* iArgv);

/**
 * @brief: parseAndDispatch.
 * @details: This command parses the data received to a proper format to dispatch for execution.
 * @param: iLineBuffer (Input) - The data to parse (Commands in improper format).
 * @return none.
 */
void parseAndDispatch(char * iLineBuffer);

/**
 * @brief: dispatchCmd.
 * @details: This command sends the command for execution after validation if command exists in path.
 * @param: iCmdArr (Input) - The data to dispatch for execution.
 * @return none.
 */
void dispatchCmd(const char **iCmdArr);

/**
 * @brief: executeCmd.
 * @details: This command executes the command by forking.
 * @param: iPath (Input) - Path for the command source.
 * @param: iCmdArr (Input) - Command to execute.
 * @return none.
 */
void executeCmd(char *iPath,char **iCmdArr);

/**
 * @brief: prepareSingleStrPath.
 * @details: This command prepares a single string from an array of individual strings.
 * @param: iArr (Input) - Array with the seperate strings.
 * @return char * - Pointer to the combines single string.
 */
char * prepareSingleStrPath(const char** iArr);