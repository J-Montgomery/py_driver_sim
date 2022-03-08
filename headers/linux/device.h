#pragma once

/* INCLUDE_BEGIN */
#include <linux/device/bus.h>
#include <linux/device/driver.h>
#include <linux/types.h>
#include <linux/gfp.h>
#include <stdlib.h>
/* INCLUDE_END */

/* STRUCT_BEGIN */
struct device {
	struct device	*parent;
	const char	*init_name;

	struct bus_type	*bus;
	void		*platform_data;
	void		*driver_data;
};
/* STRUCT_END */

/* CODE_BEGIN */
static inline void *dev_get_drvdata(const struct device *dev)
{
	return dev->driver_data;
}

static inline void dev_set_drvdata(struct device *dev, void *data)
{
	dev->driver_data = data;
}

static inline void *devm_kmalloc(struct device *dev, size_t size, gfp_t gfp)
{
	return malloc(size);
}
static inline void *devm_kzalloc(struct device *dev, size_t size, gfp_t gfp)
{
	// Our little secret
	return calloc(1, size);
}
/* CODE_END */
