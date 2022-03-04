#include <stdio.h>
#include "lib.h"


int main(int argv, char **argc) {
    printf("Hello, World!\n");

    printf("Result: %x\n", call_stub(3, 5));

    return 0;
}