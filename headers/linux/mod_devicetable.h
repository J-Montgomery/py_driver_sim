#pragma once

/* spi */

#define SPI_NAME_SIZE	32
#define SPI_MODULE_PREFIX "spi:"

struct spi_device_id {
	char name[SPI_NAME_SIZE];
	unsigned long driver_data;
};
