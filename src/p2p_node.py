from pythonp2p import Node
import socket


def get_my_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


class P2PNode(Node):

    def __init__(self, host='localhost', port=65432):
        self.player = None
        self.last_message = None
        super().__init__(host, port)
        self.start()

    def on_message(self, message, sender, private):
        if not message == self.last_message:
            self.last_message = message
            self.player.parse_message(message)

    def connect_to(self, host, port=65432):
        super().connect_to(host, port)

    def send_message(self, message, reciever=None):
        super().send_message(message, reciever)
