#include <stdio.h>
#include <linux/module.h>
#include <linux/spi/spi.h>
#include "lib.h"

void print_buf(char *buffer, size_t len) {
    for (size_t i=0; i<len; i++) {
        printf("%02x [%c] ", buffer[i], buffer[i]);
        if ((i+1)%16 == 0) printf("\n");
    }
}

int main(int argv, char **argc) {
    printf("Hello, World!\n");

    printf("Result: %i\n", call_stub(3, 5));
    printf("Result2: %i\n", call_stub2(3, 5));

    printf("sizeof: %lx\n", sizeof(const struct spi_device_id));
    return 0;
}

static const struct spi_device_id max31722_spi_id[] = {
	{"max31722", 3},
	{"max31723", 2},
    {"max31723", 1},
	{}
};
MODULE_DEVICE_TABLE(spi, max31722_spi_id);