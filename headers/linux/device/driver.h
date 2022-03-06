#pragma once

#define module_driver(__driver, __register, __unregister, ...) \
static int __attribute__((constructor)) __driver##_init(void) \
{ \
	return __register(&(__driver) , ##__VA_ARGS__); \
} \
module_init(__driver##_init); \
static void __attribute__((destructor)) __driver##_exit(void) \
{ \
	__unregister(&(__driver) , ##__VA_ARGS__); \
} \
module_exit(__driver##_exit);

struct device_driver {
	const char		*name;
};
