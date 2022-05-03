from libharness import ffi, lib
import sys

ResourceLoader(RESOURCE_STRING)
from edtlib import EDT
import json
import argparse
import time

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
    server = g_object_registry.get("ioserver", "")
    print("UART: {}".format(ffi_str(msg)))
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

@ffi.def_extern()
def harness_main(argc, argv):
    args = [ffi_str(argv[x]) for x in range(1, argc)]

    status = parse_args(args)
    if status:
        return status

    print(g_test_config)
    # Initialize the zeromq server
    # message_broker = ZmqMessageBus(g_test_config['router_uri'], g_test_config['dealer_uri'])
    # message_broker.start()

    # rep = ZmqRep(g_test_config['dealer_uri'])
    # rep.start()

    # req = ZmqReq(g_test_config['router_uri'])
    # req.send("Hello, World!")

    io_server = IOServer(g_test_config['router_uri'], g_test_config['dealer_uri'])
    uart = UartServer(io_server)

    io_server.start()
    time.sleep(1)
    io_msg = IOMessenger(g_test_config['router_uri'])
    io_msg.send('peripheral.uart.write', "test")

    g_object_registry.bind("ioserver1", "", io_server)
    g_object_registry.bind("ioserver", "", io_msg)

    # Initialize the core message broker for the system
    # Initialize the root device class, which will initialize
    #   child devices in turn
    return 0
