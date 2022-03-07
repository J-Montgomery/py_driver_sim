import cffi
import parse_headers

ffibuilder = cffi.FFI()

module_list = ["model.py"]
header_list = ["headers/known_functions.h"]

source = []

# Add all of our fake kernel header files
# header_list.extend(list(get_files("headers")))
# print(header_list)

(macro_vals, macro_funcs, structs, prototypes) = parse_headers.parse_headers("headers")


# for file in header_list:
#     with open(file) as f:
#         code = "".join([line for line in f if not line.startswith("#")])
#         source.append(code + "\n")

# code = "".join(source)
# ffibuilder.embedding_api(code)  ## needs prototypes
ffibuilder.embedding_api("\n".join(prototypes))

# Need to fix this, this is gross
# ffibuilder.set_source(
#     "model",
#     r"""
#     #define SPI_NAME_SIZE	32
# #define SPI_MODULE_PREFIX "spi:"

# struct device {
# 	struct device	*parent;
# 	const char	*init_name;
# };

# struct device_driver {
# 	const char		*name;
# };

# struct spi_device_id {
# char name[SPI_NAME_SIZE];
# unsigned long driver_data;
# };

#     struct spi_controller {
# 	struct device	dev;
# };

# struct spi_device {
# 	struct device		dev;
# 	struct spi_controller	*controller;
# 	struct spi_controller	*master;	/* compatibility layer */
# };

# struct spi_driver {
# 	const struct spi_device_id *id_table;
# 	int			(*probe)(struct spi_device *spi);
# 	int			(*remove)(struct spi_device *spi);
# 	void			(*shutdown)(struct spi_device *spi);
# 	struct device_driver	driver;
# };

# int call_probe(struct spi_driver *sdrv) {
#     return sdrv->probe(0);
# }
# """,
# )  ## needs macros, structs, enums, declarations

source = []
list(map(source.extend, [macro_vals, structs, ["int call_probe(struct spi_driver *sdrv) { return sdrv->probe(0); }"]]))
source = "\n".join(source)
ffibuilder.set_source("model", source)

# ffibuilder.cdef(
#     r"""
# #define SPI_NAME_SIZE	32

# struct device {
# 	struct device	*parent;
# 	const char	*init_name;
# };

# struct device_driver {
# 	const char		*name;
# };

# struct spi_device_id {
# char name[SPI_NAME_SIZE];
# unsigned long driver_data;
# };

#     struct spi_controller {
# 	struct device	dev;
# };

# struct spi_device {
# 	struct device		dev;
# 	struct spi_controller	*controller;
# 	struct spi_controller	*master;	/* compatibility layer */
# };

# struct spi_driver {
# 	const struct spi_device_id *id_table;
# 	int			(*probe)(struct spi_device *spi);
# 	int			(*remove)(struct spi_device *spi);
# 	void			(*shutdown)(struct spi_device *spi);
# 	struct device_driver	driver;
# };

# int call_probe(struct spi_driver *sdrv);
# """
# )  # needs macros, variables, structs, enums

source = []
list(map(source.extend, [macro_vals, structs, ["int call_probe(struct spi_driver *sdrv);"]]))
source = "\n".join(source)
ffibuilder.cdef(source)

source = []
for file in module_list:
    with open(file) as f:
        code = f.read()
        source.append(code + "\n")

code = "".join(source)
ffibuilder.embedding_init_code(code)

target_name = "model.*"

ffibuilder.compile(target=target_name, verbose=True)
