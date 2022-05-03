
from libharness import ffi
import logging
import zmq


class UartServer(object):
    def __init__(self, ioserver):
        self.ioserver = ioserver
        self.log = logging.getLogger('UartServer')
        ioserver.register_topic('peripheral.uart.write', self.write_handler)

    def write_handler(self, ioserver, msg):
        self.log.info('uart write: \'{}\''.format(msg))
        return
