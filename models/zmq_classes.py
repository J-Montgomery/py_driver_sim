from libharness import ffi
from threading import Thread
import zmq
import json

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

def encode_message(topic, data):
    msg = dict()
    msg['topic'] = topic
    msg['data'] = data
    return json.dumps(msg)

def decode_message(msg):
    msg = json.loads(msg)
    return msg['topic'], msg['data']

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
        rsp = self.socket.recv()
        print("receiving req {}".format(rsp))
        return rsp


class IOServer(Thread):
    def __init__(self, rx_uri, tx_uri):
        super().__init__()
        self.rx_uri = rx_uri
        self.tx_uri = tx_uri
        self.context = zmq.Context()

        self.rx_socket = self.context.socket(zmq.SUB)
        self.rx_socket.connect(self.rx_uri)

        self.tx_socket = self.context.socket(zmq.PUB)
        self.tx_socket.connect(self.tx_uri)

        self.handlers = {}
        print("sockets {} {}", self.rx_uri, self.tx_uri)

    def register_topic(self, topic, handler):
        print("Registering RX_Port: %s, Topic: %s" % (self.rx_uri, topic))
        topic_string = '{"topic": "' + topic + '",'
        #print("topic [{}]".format(topic_string))
        self.rx_socket.setsockopt_string(zmq.SUBSCRIBE, topic_string)
        self.handlers[topic] = handler

    def run(self):
        socket_thread = Thread(target=self.socket_poll)
        socket_thread.start()
        socket_thread.join() # unreachable

    def socket_poll(self):
        print("socket poll")
        self.poller = zmq.Poller()
        self.poller.register(self.rx_socket, zmq.POLLIN)
        print("socket poll2")
        while True:
            print("socket poll3")
            sockets = dict(self.poller.poll(1000))
            print("run ", sockets)
            if sockets.get(self.rx_socket) == zmq.POLLIN:
                msg = self.rx_socket.recv()
                topic, data = decode_message(msg)
                print("IOServer received {} {}".format(topic, data))
                handler = self.handlers[topic]
                handler(self, data)


class IOMessenger(object):
    def __init__(self, tx_uri):
        self.tx_uri = tx_uri
        self.context = zmq.Context()
        self.tx_socket = self.context.socket(zmq.PUB)
        print("binding ", self.tx_socket.bind(tx_uri))

    def send(self, topic, msg):
        print("sending to", self.tx_uri, encode_message(topic, msg))
        self.tx_socket.send_string(encode_message(topic, msg))
