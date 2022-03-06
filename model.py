from model import ffi


def get_string(cdata):
    return ffi.string(cdata).decode('ascii')

device_table = []

@ffi.def_extern()
def call_stub(x, y):
    print("stub({0}, {1})".format(x, y))
    return x + y

@ffi.def_extern()
def spi_register_driver(sdrv):
    print("register_driver", sdrv)
    return 0

@ffi.def_extern()
def spi_unregister_driver(sdrv):
    print("unregister_driver", sdrv)

# initialize_device_table(char *type, char *name, char *device_name, int device_id);
@ffi.def_extern()
def initialize_device_table(type, name, dev_name, dev_id):
    dev_entry = [get_string(type), get_string(name), get_string(dev_name), dev_id]
    print("Init device table: {}".format(dev_entry))
    device_table.append(dev_entry)


@ffi.def_extern()
def main(argv, argc):
    print("Hello, World!")
    return 0
