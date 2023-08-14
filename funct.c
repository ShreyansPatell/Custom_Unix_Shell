/**
 * @brief: funct.c
 * 
 * @paragraph: Description - Support file of tash.c. It contains all the functions that will be used by tash while execution.
 * 
 * @authors: Shreyans Patel (SSP210009), Karan Jariwala (KHJ200000).
 */

#include"funct.h"

/**
 * @brief: modifyPath.
 * @details: This is used to modify (set/update) the path variable.
 * @param: iPath (Input) - The paths to set for the path variable.
 * @return none.
 */
void modifyPath(char* iPath)
{
    if(NULL == iPath)
    {
        printErrorMsg();
        exit(0);
    }

    //This is required for overwriting the path variable.
    if(NULL != gPath)
    {
        free(gPath);
        gPath = NULL;
    }

    gPath = strdup(iPath);
}

/**
 * @brief: printErrorMsg.
 * @details: This function is used to print the one and only error message.
 * @return none.
 * @note: tTemp in this function is used to avoid compilation errors since we need to use the return value of write(). This is because of the compilation instructions being passed. Unused variables are considered errors in this case.
 */
void printErrorMsg(void)
{
    int tTemp = 0;
    tTemp = write(STDERR_FILENO,ERROR_MSG,strlen(ERROR_MSG));
    tTemp++;
}

/**
 * @brief: initTash.
 * @details: Initialization of tash program. It decides the mode of runtime i.e Interactive or Batch Mode.
 * @param: iArgc (Input) - The number of input arguments passed while executing "./tash". "./tash" counts too.
 * @param: iArgv (Input) - Array of arguments.
 * @return int.
 */
void initTash(int iArgc, char** iArgv)
{
    if(1 == iArgc)
    {
        initInteractive();  //Start tash in interactive mode.
    }
    else if(2 == iArgc)
    {
        initBatch(iArgv[iArgc-1]);  //Start tash in batch mode.
    }
    else
    {
        printErrorMsg();    //Invalid mode, show error. This is for more than one argument to ""./tash".
        exit(1);
    }
}

/**
 * @brief: initInteractive.
 * @details: Initialize interactive mode of tash.
 * @return none.
 */
void initInteractive(void)
{	
	char *tLineBuffer = NULL;
	size_t tLineBufferSize = 0;

    //If there was no redirection in input, then it must be interactive mode of operation. Then print prompt.
    if(1 == isatty(STDIN_FILENO))
    {
        printf("tash> ");
    }
	
	while ((tLineBufferSize = getline(&tLineBuffer, &tLineBufferSize, stdin) != -1))
    {
		parseAndDispatch(tLineBuffer);
        
        //If there was no redirection in input, then it must be interactive mode of operation. Then print prompt.
        if(1 == isatty(STDIN_FILENO))
        {
            printf("tash> ");
        }
    }		
}

/**
 * @brief: initBatch.
 * @details: Initialize batch mode of tash.
 * @param: iArgv (Input) - Array of argument strings.
 * @return none.
 */
void initBatch(char* iArgv)
{
    //Validation before accessing. For safety.
    if(NULL == iArgv)
    {
        printErrorMsg();
        return;
    }

    FILE *tFileHandler = NULL;
    char *tLineBuffer = NULL;
    size_t tLineBufferSize = 0;

    //Open the file.
    tFileHandler = fopen(iArgv,"r");

    //Opening the file failed.
    if(NULL == tFileHandler)
    {
        printErrorMsg();
        return;
    }
    
    //Read file line by line until end of file.
    while(1)
    {
        tLineBufferSize = getline(&tLineBuffer,&tLineBufferSize,tFileHandler);

        //If end of file is reached or if read failed.
        if(EOF == tLineBufferSize)
        {
            break;
        }

        //Send data for processing.
        parseAndDispatch(tLineBuffer);
    }

    //Close the file.
    fclose(tFileHandler);
}

/**
 * @brief: parseAndDispatch.
 * @details: This command parses the data received to a proper format to dispatch for execution.
 * @param: iLineBuffer (Input) - The data to parse (Commands in improper format).
 * @return none.
 */
void parseAndDispatch(char * iLineBuffer)
{
    //Validation before using the data.
    if((NULL == iLineBuffer))
    {
        printErrorMsg();
        return;
    }

    const char *tCmdArr[DEFAULT_CMD_BUF_SIZE];
    size_t tCmdArrIdx = 0;

    //Tokenization process related variables.
    char *tSpaceToken = NULL;
    char *tSaveSpaceToken = NULL;
    char *tAmpersandToken = NULL;
    char *tSaveAmpersandToken = NULL;
    char *tRedirectToken = NULL;
    char *tSaveRedirectToken = NULL;
    const char tSpaces[] = " \t\r\n\v\f";   //Delimiters
    const char tAmpersand[] = "&";          //Delimiters
    const char tRedirect[] = ">";           //Delimiters

    char *tValidateRedirectionStr = strdup(iLineBuffer);
    
    //This is to validate if there is no command on the left of "&". Then it is an error.
    if((NULL != strstr(tValidateRedirectionStr,"&")) && (0 == strcmp(strtok(tValidateRedirectionStr,tSpaces),"&")))
    {
        printErrorMsg();
        return;
    }

    //Tokenization for &.
    for(tAmpersandToken = strtok_r(iLineBuffer, tAmpersand, &tSaveAmpersandToken); 
        tAmpersandToken != NULL; 
        tAmpersandToken = strtok_r(NULL, tAmpersand, &tSaveAmpersandToken))
    {
        //Tokenization for whitspaces.
        for(tSpaceToken = strtok_r(tAmpersandToken, tSpaces, &tSaveSpaceToken); 
            tSpaceToken != NULL; 
            tSpaceToken=strtok_r(NULL, tSpaces, &tSaveSpaceToken)) 
        {
            if((NULL != strstr(tSpaceToken,">")) && (0 != strcmp(tSpaceToken,">")))
            {
                tRedirectToken = strtok_r(tSpaceToken, tRedirect, &tSaveRedirectToken);
                
                tCmdArr[tCmdArrIdx] = strdup(tRedirectToken);
                tCmdArrIdx++;
                tCmdArr[tCmdArrIdx] = strdup(">");
                tCmdArrIdx++;
                tRedirectToken = strtok_r(NULL, tRedirect, &tSaveRedirectToken);
                tCmdArr[tCmdArrIdx] = strdup(tRedirectToken);
                tCmdArrIdx++;
                break;
            }
            tCmdArr[tCmdArrIdx] = strdup(tSpaceToken);
            tCmdArrIdx++;
        }

        tCmdArr[tCmdArrIdx] = NULL;

        dispatchCmd(tCmdArr);

        tCmdArrIdx = 0;
    }
}

/**
 * @brief: dispatchCmd.
 * @details: This command sends the command for execution after validation if command exists in path.
 * @param: iCmdArr (Input) - The data to dispatch for execution.
 * @return none.
 */
void dispatchCmd(const char **iCmdArr)
{
    if(NULL == iCmdArr[0])
    {
        return;
    }

    //Built-in Command - exit.
    if(0 == strcmp("exit",iCmdArr[0]))
    {
        if(NULL != iCmdArr[1])
        {
            printErrorMsg();
            return;
        }

        exit(0);
    }

    //Built-in Command - path.
    if(0 == strcmp("path",iCmdArr[0]))
    {
        char *tPath = NULL;

        tPath = prepareSingleStrPath(iCmdArr);

        if(NULL == tPath)
        {
            return;
        }
        
        modifyPath(tPath);
        return;
    }
    
    ////Built-in Command - cd.
    if(0 == strcmp("cd",iCmdArr[0]))
    {
        if((NULL != iCmdArr[2]) || (-1 == chdir(iCmdArr[1])))
        {
            printErrorMsg();
        }
        return;
    }

    int tIsCmdFound = -1;   //To check if the path variable has the command user is trying to execute.
    char *tFinalPath = NULL;
    char *tCmdPath = strdup(gPath);

    char *tSpaceToken = NULL;
    char *tSaveSpaceToken = NULL;
    const char tSpaces[] = " \t\r\n\v\f";   //Delimiters

    //Tokenization for Spaces.
    for(tSpaceToken = strtok_r(tCmdPath, tSpaces, &tSaveSpaceToken); tSpaceToken != NULL; tSpaceToken = strtok_r(NULL, tSpaces, &tSaveSpaceToken))
    {
        tFinalPath = (char *) malloc((sizeof(tSpaceToken) + sizeof(iCmdArr[0]) + 2) * sizeof(char *)); 
        strcpy(tFinalPath,tSpaceToken);
        strcat(tFinalPath,"/");
        strcat(tFinalPath,iCmdArr[0]);

        tIsCmdFound = access(tFinalPath, X_OK);

        //If command is present at the given path, execute it.
        if(0 == tIsCmdFound)
        {
            executeCmd(tFinalPath,(char**)iCmdArr);
            break;
        }
    }
    
    //Command not found in the path. Show error.
    if(-1 == tIsCmdFound)
    {
        printErrorMsg();
    }
}

/**
 * @brief: executeCmd.
 * @details: This command executes the command by forking.
 * @param: iPath (Input) - Path for the command source.
 * @param: iCmdArr (Input) - Command to execute.
 * @return none.
 */
void executeCmd(char *iPath,char **iCmdArr)
{
    pid_t tPid, tWaitPid;
    int tStatus;

    tPid = fork();

    //Forking failed, give error and return.
    if(tPid < 0)
    {
        printErrorMsg();
        exit(0);
    }

    //Child Loop.
    else if(0 == tPid)
    {
        int tIndex = 0;
        int tRedirectionCnt = 0;
        int tRedirectionFileNameIdx = 0;

        //Check if output is to be redirected.
        while(NULL != iCmdArr[tIndex])
        {
            //If two or more ">" in an argument, it is an error.
            if(NULL != strstr(iCmdArr[tIndex],">>"))
            {
                printErrorMsg();
                return;
            }

            //If one ">" is found, redirection is possible, do the needed validations.
            if (0 == strcmp(iCmdArr[tIndex],">"))
            {
                tRedirectionCnt++;
                
                tRedirectionFileNameIdx = tIndex + 1;

                if((NULL == iCmdArr[tIndex + 1]) || (NULL != iCmdArr[tIndex + 2]))
                {
                    printErrorMsg();
                    return;
                }
            }
            tIndex++;
        }
        
        //More than one redirection symbol used.
        if(1 < tRedirectionCnt)
        {
            printErrorMsg();
            return;
        }

        //Valid redirection, prepare the output file name from next argument.
        else if(1 == tRedirectionCnt)
        {
            char *tOutputPath = NULL;
            tOutputPath = strdup(iCmdArr[tRedirectionFileNameIdx]);
            close(STDOUT_FILENO);
            open(tOutputPath, O_CREAT | O_WRONLY | O_TRUNC, S_IRWXU);
            iCmdArr[tRedirectionFileNameIdx-1] = NULL;
            iCmdArr[tRedirectionFileNameIdx] = NULL;
        }
        
        //Execv failed.
        if(-1 == execv(iPath,iCmdArr))
        {
            printErrorMsg();
            return;
        }
    }

    //Parent Process.
    else
    {
        do
        {
            tWaitPid = waitpid(tPid, &tStatus, WUNTRACED);
        } 
        while (!WIFEXITED(tStatus) && !WIFSIGNALED(tStatus));

        tWaitPid++;
    }
}

/**
 * @brief: prepareSingleStrPath.
 * @details: This command prepares a single string from an array of individual strings.
 * @param: iArr (Input) - Array with the seperate strings.
 * @return char * - Pointer to the combines single string.
 */
char * prepareSingleStrPath(const char** iArr)
{
    //Validation if array passed is null.
    if (iArr == NULL)
    {
        return NULL;
    }

    int tLoopIndex = 1;    //Loop index for array. It starts from 1 since the 0th index will have path command.
    int tCount = 0;         //Used to count the number of elements for setting as paths.
    char *tResult = NULL;   //Result string which is a combination of all element strings.
    int tTotalLength = 0;   //Length of the result string.

    //Iterate through the array to count as well as get the total length required for final string including spaces and NULL termination.
    while (iArr[tLoopIndex] != NULL)
    {
        tTotalLength += (strlen(iArr[tLoopIndex]) + 1); //Consider space after everypath that is entered so +1.
        tLoopIndex++;
    }

    //Update the count variable.
    tCount = tLoopIndex;

    //Allocate required memory to the final string.
    tResult = malloc(tTotalLength * sizeof(char *));

    //Memory allocation failed.
    if (tResult == NULL) 
    {
        return NULL;
    }

    //Concatenate the individual elements of the array to form the final string.
    for (tLoopIndex = 1; tLoopIndex < tCount; tLoopIndex++) 
    {
        strcat(tResult, iArr[tLoopIndex]);
        strcat(tResult, " ");
    }
    
    return tResult;
}