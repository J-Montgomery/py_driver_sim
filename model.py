from model import ffi, lib


from inspect import getmembers

def get_string(cdata):
    return ffi.string(cdata).decode('ascii')

def cdata_dict(cd):
    if isinstance(cd, ffi.CData):
        try:
            return ffi.string(cd)
        except TypeError:
            try:
                return [cdata_dict(x) for x in cd]
            except TypeError:
                return {k: cdata_dict(v) for k, v in getmembers(cd)}
    else:
        return cd

device_table = dict()

driver_table = dict()

def find_device_table(entry):
    name = entry['name'].decode('ascii')
    for driver in device_table:
        devices = device_table[driver]
        for dev in devices:
            if name in dev:
                print("found!", entry, dev, driver)
                return driver

@ffi.def_extern()
def call_stub(x, y):
    print("stub({0}, {1})".format(x, y))
    return x + y

@ffi.def_extern()
def spi_register_driver(sdrv):
    driver = cdata_dict(sdrv[0])
    print("register_driver", sdrv, driver['id_table'])
    drv = find_device_table(driver['id_table'])
    driver_table[drv] = sdrv
    return 0

@ffi.def_extern()
def spi_unregister_driver(sdrv):
    print("unregister_driver", sdrv)

@ffi.def_extern()
def initialize_device_table(type, name, dev_name, dev_id):
    key = get_string(name)
    dev_entry = [get_string(dev_name), dev_id]
    if key in device_table:
        device_table[key].append(dev_entry)
    else:
        device_table[key] = [dev_entry]
    print("Init device table ({} : {}".format(key, dev_entry))
    print(device_table)


@ffi.def_extern()
def main(argv, argc):
    print("Hello, World!")
    if not len(driver_table):
        print("No drivers found")
    else:
        drivers = [driver_table[x] for x in driver_table]
        print("driver ", drivers)
        # attempt to probe the first driver
        lib.call_probe(drivers[0])
    return 0
