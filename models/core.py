from libharness import ffi, lib
import sys

ResourceLoader(RESOURCE_STRING)
from edtlib import EDT
import json
import argparse
import time
import logging

g_test_config = None
g_object_registry = ObjectRegistry()

def ffi_str(s):
    return ffi.string(s).decode('utf-8')

@ffi.def_extern()
def call_stub(x, y):
    print("stub({0}, {1})".format(x, y))
    return x + y

@ffi.def_extern()
def uart_write(msg, len):
    server = g_object_registry.get("frontend")
    #print("UART: {}".format(ffi_str(msg)))
    server.send('peripheral.uart.write', ffi_str(msg))
    return len

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

def init_stdout_logger():
    loglevel = logging.INFO
    root = logging.getLogger()
    root.setLevel(loglevel)
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(loglevel)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

@ffi.def_extern()
def harness_main(argc, argv):
    args = [ffi_str(argv[x]) for x in range(1, argc)]

    init_stdout_logger()

    status = parse_args(args)
    if status:
        return status

    print(g_test_config)

    # Initialize the zeromq server
    backend = ZmqBackend(g_test_config['router_uri'], g_test_config['dealer_uri'])
    uart = UartServer(backend)
    backend.start()

    frontend = ZmqFrontend(g_test_config['router_uri'])
    frontend.send('peripheral.uart.write', "test")

    g_object_registry.bind("frontend", frontend)

    # Initialize the core message broker for the system
    # Initialize the root device class, which will initialize
    #   child devices in turn
    return 0
