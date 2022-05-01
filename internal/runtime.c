/* INCLUDE_BEGIN */
#include <stdlib.h>
#include "parahost.h"
/* INCLUDE_END */

/* CODE_BEGIN */
extern int harness_main(int argc, char *argv[]);

__attribute__((constructor)) int init(int argc, char **argv, char **envp)
{
	int status = harness_main(argc, argv);
	if(status)
		exit(status);
	return status;
}
/* CODE_END */
