#pragma once

/* MACRO_VALUE_BEGIN */
#define SPI_NAME_SIZE	32
/* MACRO_VALUE_END */

/* MACRO_FUNC_BEGIN */
#define SPI_MODULE_PREFIX "spi:"
/* MACRO_FUNC_END */

/* STRUCT_BEGIN */
struct spi_device_id {
	char name[SPI_NAME_SIZE];
	unsigned long driver_data;
};
/* STRUCT_END */
