from pythonp2p import Node
from pythonp2p.node import PORT


class P2PNode(Node):

    def __init__(self, host='localhost'):
        super().__init__(host)
        self.buffer = []
        self.start()

    def on_message(self, message, sender, private):
        self.buffer.append(message)

    def connect_to(self, host, port=PORT):
        super().connect_to(host, port)

    def send_message(self, message, reciever=None):
        super().send_message(message, reciever)
        while not self.buffer:
            pass

        return self.buffer.pop()


