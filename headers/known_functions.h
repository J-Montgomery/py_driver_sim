#pragma once

/* INCLUDE_BEGIN */
#include "linux/spi/spi.h"
/* INCLUDE_END */

/* PROTOTYPE_BEGIN */
extern void initialize_device_table(char *type, char *name, const char *device_name, int device_id);
extern int main(int argc, char **argv);
extern int spi_register_driver(struct spi_driver *sdrv);
extern void spi_unregister_driver(struct spi_driver *sdrv);
extern int call_stub(int x, int y);
/* PROTOTYPE_END */
