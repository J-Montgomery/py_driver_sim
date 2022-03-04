#include <stdio.h>
#include "lib.h"


int main(int argv, char **argc) {
    printf("Hello, World!");

    printf("Result: %x\n", call_stub(0, 1));

    return 0;
}