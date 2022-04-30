from libharness import ffi
from threading import Thread
import zmq


# [ REQ ]  [ REQ ] [ REQ ]
#    |        |       |
#    +--------+-------+
#             |
#         [ Router ]
#         [ Dealer ]
#             |
#    +--------+-------+
#    |        |       |
# [ REP ]  [ REP ] [ REP ]

class ZmqMessageBus(Thread):
    def __init__(self, router_uri, dealer_uri, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("ZeroMQ Broker init ", router_uri, dealer_uri)

        self.context = zmq.Context()
        self.router_uri = router_uri
        self.router_socket = self.context.socket(zmq.ROUTER)
        self.router_socket.bind(self.router_uri)

        self.dealer_uri = dealer_uri
        self.dealer_socket = self.context.socket(zmq.DEALER)
        self.dealer_socket.bind(self.dealer_uri)

        self.poller = zmq.Poller()
        self.poller.register(self.router_socket, zmq.POLLIN)
        self.poller.register(self.dealer_socket, zmq.POLLIN)

    def socket_poll(self):
        while(True):
            sockets = dict(self.poller.poll())
            if sockets.get(self.router_socket) == zmq.POLLIN:
                message = self.router_socket.recv_multipart()
                self.dealer_socket.send_multipart(message)

            if sockets.get(self.dealer_socket) == zmq.POLLIN:
                message = self.dealer_socket.recv_multipart()
                self.router_socket.send_multipart(message)

    def run(self):
        socket_thread = Thread(target=self.socket_poll)
        socket_thread.start()
        socket_thread.join() # unreachable
