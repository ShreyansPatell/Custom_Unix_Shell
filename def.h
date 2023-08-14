/**
 * @brief: def.h
 * 
 * @paragraph: Description - Support file of tash.c. It contains all the definitions that will be used by tash while execution.
 * 
 * @authors: Shreyans Patel (SSP210009), Karan Jariwala (KHJ200000)
 */

//Definitions.
#define ERROR_MSG "An error has occurred\n"  //The one and only error message of the program.
#define DEFAULT_PATH "/bin"     //Path variable.
#define DEFAULT_CMD_BUF_SIZE 1024   //Size of command buffer.

//Global Variables.
char* gPath = NULL;     //Global path variable.