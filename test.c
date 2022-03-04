#include <stdio.h>
#include "lib.h"


int main(int argv, char **argc) {
    printf("Hello, World!\n");

    printf("Result: %i\n", call_stub(3, 5));
    printf("Result2: %i\n", call_stub2(3, 5));

    return 0;
}