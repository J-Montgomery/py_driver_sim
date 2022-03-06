#pragma once

#include <linux/device/driver.h>

struct device {
	struct device	*parent;
	const char	*init_name;
};
