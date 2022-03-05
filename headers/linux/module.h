#pragma once

#include <linux/stringify.h>
#include <stdio.h>

extern void initialize_device_table(char *driver_name, char *device_name, int device_id);

#define MODULE_LICENSE(_license)
#define MODULE_AUTHOR(_author)
#define MODULE_DESCRIPTION(_desc)

#define MODULE_DEVICE_TABLE(type, name) \
extern const typeof(name) __mod_##type##__##name##_device_table   __attribute__ ((unused, alias(__stringify(name)))); \
void __attribute__((constructor)) construct_##name(void) { \
    size_t len = sizeof(typeof(name)) / sizeof(typeof(name[0])); \
    void *ptr = (void *)name; \
    for(size_t i = 0; i < len; i++) { \
        typeof(name[0]) entry = *(typeof(name[0]) *)(ptr + sizeof(typeof(name[0])) * i); \
        printf("dev: %p %s %s %lu\n", ptr + sizeof(typeof(name[0])) * i, __stringify(name), entry.dev, entry.driver_data); \
    } \
}


// initialize_device_table(__stringify(name), entry.dev, entry.driver_data);