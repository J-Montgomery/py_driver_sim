#pragma once

#include <known_functions.h>
#include <linux/stringify.h>
#include <stdio.h>

#define MODULE_LICENSE(_license)
#define MODULE_AUTHOR(_author)
#define MODULE_DESCRIPTION(_desc)

#define module_init(init)
#define module_exit(exit)

#define MODULE_DEVICE_TABLE(__devtype, __devname) \
extern const typeof(__devname) __mod_##__devtype##__##__devname##_device_table   __attribute__ ((unused, alias(__stringify(__devname)))); \
	void __attribute__((constructor)) construct_##__devname(void) { \
		size_t len = sizeof(typeof(__devname)) / sizeof(typeof(__devname[0])); \
		void *ptr = (void *)__devname; \
		for(size_t i = 0; i < (len - 1); i++) { \
			typeof(__devname[0]) entry = *(typeof(__devname[0]) *)(ptr + sizeof(typeof(__devname[0])) * i); \
			initialize_device_table(__stringify(type), __stringify(__devname), entry.name, entry.driver_data); \
		} \
	}
