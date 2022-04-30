/* INCLUDE_BEGIN */
#include <stdlib.h>
#include "lib.h"
/* INCLUDE_END */

/* CODE_BEGIN */
int uart_write(char *string, int len)
{
	printf("UART: %s", string);
	return 0;
}


__attribute__((constructor)) int init(int argc, char **argv, char **envp)
{
	int status = harness_main(argc, argv);
	if(status)
		exit(status);
	return status;
}
/* CODE_END */
