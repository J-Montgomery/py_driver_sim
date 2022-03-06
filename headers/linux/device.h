#pragma once

/* INCLUDE_BEGIN */
#include <linux/device/driver.h>
/* INCLUDE_END */

/* STRUCT_BEGIN */
struct device {
	struct device	*parent;
	const char	*init_name;
};
/* STRUCT_END */
