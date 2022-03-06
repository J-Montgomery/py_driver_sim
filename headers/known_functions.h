#pragma once

#include "linux/spi/spi.h"

extern void initialize_device_table(char *type, char *name, const char *device_name, int device_id);
extern int main(int argc, char **argv);
extern int spi_register_driver(struct spi_driver *sdrv);
extern void spi_unregister_driver(struct spi_driver *sdrv);
