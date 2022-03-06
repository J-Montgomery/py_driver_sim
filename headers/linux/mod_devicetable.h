#pragma once

/* MACRO_BEGIN */
#define SPI_NAME_SIZE	32
#define SPI_MODULE_PREFIX "spi:"
/* MACRO_END */

/* STRUCT_BEGIN */
struct spi_device_id {
	char name[SPI_NAME_SIZE];
	unsigned long driver_data;
};
/* STRUCT_END */
