#include <stdio.h>
#include <linux/spi/spi.h>
#include <linux/module.h>
#include "lib.h"

void print_buf(char *buffer, size_t len) {
	for (size_t i=0; i<len; i++) {
		printf("%02x [%c] ", buffer[i], buffer[i]);
		if ((i+1)%16 == 0) printf("\n");
	}
}

int max31722_do_stuff(void) {
	printf("Hello, World!\n");

	printf("Result: %i\n", call_stub(3, 5));

	return 0;
	}

static int max31722_probe(struct spi_device *spi)
{
	printf("probing\n");
	max31722_do_stuff();
	return 0;
}

static int max31722_remove(struct spi_device *spi)
{
	printf("removing\n");
	return 0;
}

static const struct spi_device_id max31722_spi_id[] = {
	{"max31722", 1},
	{"max31723", 2},
	{"max31724", 3},
	{}
};
MODULE_DEVICE_TABLE(spi, max31722_spi_id);

static struct spi_driver max31722_driver = {
	.driver = {
		.name = "max31722",
	},
	.probe =            max31722_probe,
	.remove =           max31722_remove,
	.id_table =         max31722_spi_id,
};

module_spi_driver(max31722_driver);

MODULE_AUTHOR("Tiberiu Breana <tiberiu.a.breana@intel.com>");
MODULE_DESCRIPTION("max31722 sensor driver");
MODULE_LICENSE("GPL v2");
