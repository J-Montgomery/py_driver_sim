#include <stdio.h>
#include <linux/kernel.h>
#include <linux/spi/spi.h>
#include <linux/module.h>
#include "lib.h"

struct device_data {
	struct spi_device *spi_device;
};

int device_do_stuff(void) {
	printf("Hello, World!\n");

	printf("Result: %i\n", call_stub(3, 5));

	return 0;
	}

static int device_probe(struct spi_device *spi)
{
	int ret;
	struct device_data *data;

	printf("probing %p\n", spi);

	data = devm_kzalloc(&spi->dev, sizeof(*data), GFP_KERNEL);
	if (!data)
		return -ENOMEM;

	spi_set_drvdata(spi, data);
	data->spi_device = spi;

	device_do_stuff();
	return 0;
}

static int device_remove(struct spi_device *spi)
{
	printf("removing\n");
	return 0;
}

static const struct spi_device_id device_spi_id[] = {
	{"vendor,devicev1", 1},
	{"vendor,devicev2", 2},
	{"vendor,devicev3", 3},
	{}
};
MODULE_DEVICE_TABLE(spi, device_spi_id);

static struct spi_driver device_driver = {
	.driver = {
		.name = "device",
	},
	.probe =            device_probe,
	.remove =           device_remove,
	.id_table =         device_spi_id,
};

module_spi_driver(device_driver);

MODULE_AUTHOR("Foo Bar <foo@bar.com>");
MODULE_DESCRIPTION("Generic SPI sensor driver");
MODULE_LICENSE("GPL v2");
