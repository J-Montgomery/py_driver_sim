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

    def socket_poll(self):
        self.poller = zmq.Poller()
        self.poller.register(self.router_socket, zmq.POLLIN)
        self.poller.register(self.dealer_socket, zmq.POLLIN)
        while(True):
            sockets = dict(self.poller.poll())
            if sockets.get(self.router_socket) == zmq.POLLIN:
                message = self.router_socket.recv_multipart()
                self.dealer_socket.send_multipart(message)
                print(f"router sending {message}")

            if sockets.get(self.dealer_socket) == zmq.POLLIN:
                message = self.dealer_socket.recv_multipart()
                self.router_socket.send_multipart(message)
                print(f"dealer sending {message}")

    def run(self):
        socket_thread = Thread(target=self.socket_poll)
        socket_thread.start()
        socket_thread.join() # unreachable

class ZmqRep(Thread):
    def __init__(self, dealer_uri, *args, **kwargs):
        super().__init__(*args, **kwargs)

        print("ZeroMQ Rep init ", dealer_uri)

        self.context = zmq.Context()
        self.dealer_uri = dealer_uri
        self.socket = self.context.socket(zmq.REP)
        self.socket.connect(self.dealer_uri)

    def recv(self):
        while(True):
            message = self.socket.recv()
            print("receiving req {}".format(message))
            self.socket.send(message)


    def run(self):
        socket_thread = Thread(target=self.recv)
        socket_thread.start()
        socket_thread.join() # unreachable

class ZmqReq:
    def __init__(self, router_uri):
        print("ZeroMQ Req init ", router_uri)

        self.context = zmq.Context()
        self.router_uri = router_uri
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect(self.router_uri)

    def send(self, message):
        print(f"sending req {message}")
        self.socket.send_string(message)
        print("receiving req {}".format(self.socket.recv()))
