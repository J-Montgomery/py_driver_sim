from libharness import ffi, lib
import sys

#from models.utility import device_class

ResourceLoader(RESOURCE_STRING)
from edtlib import EDT
import zmq
import json
import argparse


def get_string(cdata):
    return ffi.string(cdata).decode("ascii")


device_table = dict()
driver_table = dict()
g_test_config = None


def find_device_table(entry):
    name = entry["name"].decode("ascii")
    print(device_table)
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

# @ffi.def_extern()
# def spi_register_driver(sdrv):
#     driver = cdata_dict(sdrv[0])
#     print("register_driver", sdrv, driver["id_table"])
#     drv = find_device_table(driver["id_table"])
#     driver_table[drv] = sdrv
#     return 0

# @ffi.def_extern()
# def spi_unregister_driver(sdrv):
#     print("unregister_driver", sdrv)


# @ffi.def_extern()
# def initialize_device_table(type, name, dev_name, dev_id):
#     key = get_string(name)
#     dev_entry = [get_string(dev_name), dev_id]
#     if key in device_table:
#         device_table[key].append(dev_entry)
#     else:
#         device_table[key] = [dev_entry]
#     print("Init device table ({} : {}".format(key, dev_entry))
#     print(device_table)

def parse_dt(path):
    edt = EDT(path, '')

    # Get the DT nodes that declare a compatible string
    device_nodes = edt.compat2nodes
    for compat in device_nodes:
        if "pysim" in compat:
            print("Pysim: {}".format(compat))
        else:
            print("device: {}".format(compat))
    #print(edt.compat2nodes)
    return edt.compat2nodes

def parse_args(argv):
    parser = argparse.ArgumentParser(description="Parahosted test executable")
    parser.add_argument('config', help="Test config json")
    try:
        args = parser.parse_args(argv)
    except:
        return 1
    print(args)
    with open(args.config) as config:
        global g_test_config
        g_test_config = json.load(config)

    return 0

@ffi.def_extern()
def harness_main(argc, argv):
    args = [ffi.string(argv[x]).decode('utf-8') for x in range(1, argc)]

    status = parse_args(args)
    if status:
        return status
    
    # Initialize the zeromq server
    # foo()
    # Initialize the core message broker for the system

    # Initialize the root device class, which will initialize
    #   child devices in turn

# @ffi.def_extern()
# def main(argv, argc):
#     global_mem_pool = []
#     dt_nodes = parse_dt("test_setup.dts")

#     # Initialize our simulated devices
#     p = DeviceClass()
#     p.get_subclasses()
#     #print(_dev_id_registry)

#     p.build_id_table()

#     # traverse the device-tree and initialize our simulated devices
#     for id in dt_nodes:
#         p.call_sim_probe(id)

#     print("Starting execution\n----------------------------------------")
#     if not len(driver_table):
#         print("No drivers found")
#     else:
#         drivers = [driver_table[x] for x in driver_table]
#         #print("driver ", drivers)
#         # attempt to probe the first driver
#         mem = ffi.new("struct spi_device *")
#         global_mem_pool.append(mem)
#         lib.spi_call_probe(drivers[0], mem)
#     return 0
