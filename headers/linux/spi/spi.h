#pragma once

/* INCLUDE_BEGIN */
#include <linux/device.h>
#include <linux/mod_devicetable.h>
/* INCLUDE_END */

/* MACRO_FUNC_BEGIN */
#define module_spi_driver(__spi_driver) \
	module_driver(__spi_driver, spi_register_driver, spi_unregister_driver)
/* MACRO_FUNC_END */

/* STRUCT_BEGIN */
struct spi_controller {
	struct device	dev;
};

struct spi_device {
	struct device		dev;
	struct spi_controller	*controller;
	struct spi_controller	*master;	/* compatibility layer */
};

struct spi_driver {
	const struct spi_device_id *id_table;
	int			(*probe)(struct spi_device *spi);
	int			(*remove)(struct spi_device *spi);
	void			(*shutdown)(struct spi_device *spi);
	struct device_driver	driver;
};

/* STRUCT_END */
