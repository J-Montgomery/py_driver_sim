import cffi
import parse_headers

ffibuilder = cffi.FFI()

module_list = ["model.py"]
header_list = ["headers/known_functions.h"]

source = []
(macro_vals, macro_funcs, structs, prototypes) = parse_headers.parse_headers("headers")

ffibuilder.embedding_api("\n".join(prototypes))

source = []
list(map(source.extend, [macro_vals, structs, ["int call_probe(struct spi_driver *sdrv) { return sdrv->probe(0); }"]]))
source = "\n".join(source)
ffibuilder.set_source("model", source)

source = []
list(map(source.extend, [macro_vals, structs, ["int call_probe(struct spi_driver *sdrv);"]]))
source = "\n".join(source)
ffibuilder.cdef(source)

# Concat all the python models together
source = []
for file in module_list:
    with open(file) as f:
        code = f.read()
        source.append(code + "\n")

code = "".join(source)
ffibuilder.embedding_init_code(code)

target_name = "model.*"

ffibuilder.compile(target=target_name, verbose=True)
