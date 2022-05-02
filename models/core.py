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
    handler = g_object_registry.get(b"uart", "uart_write")
    print("UART: {}".format(ffi_str(msg)))
    print(handler.send(b'uart', ffi_str(msg).encode('utf-8')))
    response = handler.recv_all_as_list(timeout=10)
    print(response)
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

def init_logger():
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    root.addHandler(handler)

@ffi.def_extern()
def harness_main(argc, argv):
    args = [ffi_str(argv[x]) for x in range(1, argc)]

    status = parse_args(args)
    if status:
        return status

    print(g_test_config)
    init_logger()
    # Initialize the zeromq server
    # message_broker = ZmqMessageBus(g_test_config['router_uri'], g_test_config['dealer_uri'])
    # message_broker.start()

    # rep = ZmqRep(g_test_config['dealer_uri'])
    # rep.start()

    # req = ZmqReq(g_test_config['router_uri'])
    # req.send("Hello, World!")
    broker = Broker(g_test_config['router_uri'])
    broker.start()

    worker = Worker(g_test_config['router_uri'], b'uart')
    worker.connect()

    task = WorkerTask(worker)
    task.start()

    client = Client(g_test_config['router_uri'])
    client.connect()
    client.send(b'uart', b"Hello, World!")

    response = client.recv_all_as_list(timeout=10)

    g_object_registry.bind(b"uart", "uart_write", client)

    # Initialize the core message broker for the system
    # Initialize the root device class, which will initialize
    #   child devices in turn
    return 0
