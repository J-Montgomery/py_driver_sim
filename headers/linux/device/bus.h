#pragma once

/* STRUCT_BEGIN */
struct bus_type {
	const char	*name;
	const char	*dev_name;
	struct device	*dev_root;
};
/* STRUCT_END */
